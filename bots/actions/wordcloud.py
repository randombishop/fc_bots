from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
from bots.iaction import IAction
from bots.data.bq import dry_run
from bots.data.fid_features import get_words_dict_sql, get_words_dict
from bots.utils.prompts import instructions_and_request, parse_user_examples
from bots.utils.llms import call_llm
from bots.utils.read_params import read_fid
from bots.utils.images import make_wordcloud
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts


parse_instructions = """
INSTRUCTIONS:
Extract the user name from the query.
Your goal is not to answer the query, you only need to extract the user parameter.

"""
parse_instructions += parse_user_examples
parse_instructions += """

RESPONSE FORMAT:
{{
  "user": ...
}}
(if you can not extract a user name, return a json with an error message)
"""


class Wordcloud(IAction):
  
  def parse(self, input, fid_origin=None):
    prompt = instructions_and_request(parse_instructions, input, fid_origin)
    self.params = call_llm(prompt)
    self.fid = read_fid(self.params)

  def get_cost(self):
    sql, params = get_words_dict_sql(self.fid)
    test = dry_run(sql, params)
    self.cost = test['cost']
    return self.cost

  def execute(self):
    words = get_words_dict(self.fid)
    if words is None or len(words) == 0:
      raise Exception(f"Not enough activity to buid a word cloud.")
    self.data = words
    return self.data
    
  def get_casts(self, intro=''):
    filename = str(uuid.uuid4())+'.png'
    make_wordcloud(self.data, filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    cast = {
      'text': "'s wordcloud", 
      'mentions': [self.fid], 
      'mentions_pos': [0],
      'mentions_ats': [f"@{self.params['user']}"],
      'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"]
    }
    casts =  [cast]
    check_casts(casts)
    self.casts = casts
    return self.casts


if __name__ == "__main__":
  input = sys.argv[1]
  action = Wordcloud()
  action.parse(input)
  print(f"FID: {action.fid}")
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
