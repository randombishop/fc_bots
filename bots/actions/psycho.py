from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
from bots.iaction import IAction
from bots.data.casts import get_casts_for_fid
from bots.utils.prompts import instructions_and_request, extract_user_prompt
from bots.utils.llms import call_llm
from bots.utils.read_params import read_fid
from bots.utils.check_casts import check_casts

instructions = """
INSTRUCTIONS:
The text above are extracts from {user}.
Based on their posts, generate a psycho analysis about them in 3 sentences, including references to psychological pathologies, even if they don't really make sense.
You are highly encouraged to be absurd, quote them and use random emojis as you make fun of their psychological issues.

RESPONSE FORMAT:
{{
  "sentence1": "...",
  "sentence2": "...",
  "sentence3": "..."
}}
"""


class Psycho(IAction):
  
  def set_input(self, input):
    prompt = instructions_and_request(extract_user_prompt, input, self.fid_origin)
    params = call_llm(prompt)
    self.input = input
    self.set_params(params)

  def set_params(self, params):
    self.user = params['user']
    self.fid = read_fid(params)
    
  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    df = get_casts_for_fid(self.fid)
    if df is None or len(df) == 0:
      raise Exception(f"Not enough activity to buid a psychodegen analysis.")
    self.data = list(df['text'])
    return self.data
    
  def get_casts(self, intro=''):
    text = "\n".join([str(x) for x in self.data])
    prompt = text + '\n\n' + instructions.format(user=self.user) ;
    result = call_llm(prompt)
    casts = []
    if 'sentence1' in result:
      casts.append({'text': result['sentence1']})
    if 'sentence2' in result:
      casts.append({'text': result['sentence2']})
    if 'sentence3' in result:
      casts.append({'text': result['sentence3']})
    check_casts(casts)
    self.casts = casts
    return casts

if __name__ == "__main__":
  input = sys.argv[1]
  action = Psycho()
  action.set_input(input)
  print(f"FID: {action.fid}")
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.get_data()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
