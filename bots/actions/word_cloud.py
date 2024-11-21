from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
from bots.iaction import IAction
from bots.data.users import get_words_dict
from bots.utils.prompts import parse_user_instructions, parse_user_schema
from bots.utils.llms import call_llm
from bots.utils.read_params import read_fid, read_username
from bots.utils.images import make_wordcloud
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts



class WordCloud(IAction):
  
  
  def set_input(self, input):
    instructions = parse_user_instructions(self.fid_origin)
    params = call_llm(input, instructions, parse_user_schema)
    self.input = input
    self.set_params(params)

  def set_params(self, params):
    self.user = read_username(params)
    self.fid = read_fid(params)

  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
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
      'mentions_ats': [f"@{self.user}"],
      'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"]
    }
    casts =  [cast]
    check_casts(casts)
    self.casts = casts
    return self.casts


if __name__ == "__main__":
  input = sys.argv[1]
  action = WordCloud()
  action.set_input(input)
  action.run()
  action.print()
