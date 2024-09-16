from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
from bots.iaction import IAction
from bots.data.bq import dry_run
from bots.data.casts import text_for_fid_sql, text_for_fid_results
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
  
  def parse(self, input, fid_origin=None):
    prompt = instructions_and_request(extract_user_prompt, input, fid_origin)
    self.params = call_llm(prompt)
    self.fid = read_fid(self.params)

  def get_cost(self):
    sql, params = text_for_fid_sql(self.fid, 15)
    test = dry_run(sql, params)
    self.cost = test['cost']
    return self.cost

  def execute(self):
    text = text_for_fid_results(self.fid, 15)
    if text is None or len(text) == 0:
      raise Exception(f"Not enough activity to buid a psychodegen analysis.")
    self.data = text
    return self.data
    
  def get_casts(self, intro=''):
    text = "\n".join(self.data)
    prompt = text + '\n\n' + instructions.format(user=self.params['user']) ;
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
  action.parse(input)
  print(f"FID: {action.fid}")
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
