from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
from bots.iaction import IAction
from bots.data.users import get_words_dict
from bots.utils.prompts import instructions_and_request, extract_user_prompt
from bots.utils.llms import call_llm
from bots.utils.read_params import read_fid
from bots.utils.images import make_wordcloud
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts


debug = False


class PrefsCloud(IAction):
  
  
  def set_input(self, input):
    prompt = instructions_and_request(extract_user_prompt, input, self.fid_origin)
    params = call_llm(prompt)
    self.set_params(params)

  def set_params(self, params):
    self.user = params['user']
    self.fid = read_fid(params)

  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    words = get_words_dict(self.fid)
    if debug:
      print('words', words)
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
  action = PrefsCloud()
  action.set_input(input)
  print(f"FID: {action.fid}")
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.get_data()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
