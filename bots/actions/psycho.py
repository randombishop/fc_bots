from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
from bots.iaction import IAction
from bots.data.casts import get_casts_for_fid
from bots.utils.prompts import parse_user_instructions, parse_user_schema
from bots.utils.llms import call_llm
from bots.utils.read_params import read_fid, read_username
from bots.utils.check_casts import check_casts

instructions = """
INSTRUCTIONS:
- The text above are extracts from ?.
- Based on their posts, generate a psycho analysis about them in 3 sentences, including references to psychological pathologies, even if they don't really make sense.
- You are highly encouraged to be absurd, quote them and use random emojis as you make fun of their psychological issues.
- Output the result in json format.
- Make sure you don't use " inside json strings. Avoid invalid json.

RESPONSE FORMAT:
{
  "sentence1": "...",
  "sentence2": "...",
  "sentence3": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "sentence1":{"type":"STRING"},
    "sentence2":{"type":"STRING"},
    "sentence3":{"type":"STRING"}
  }
}

class Psycho(IAction):
  
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
    df = get_casts_for_fid(self.fid)
    if df is None or len(df) == 0:
      raise Exception(f"Not enough activity to buid a psychodegen analysis.")
    self.data = list(df['text'])
    return self.data
    
  def get_casts(self, intro=''):
    text = "\n".join([str(x) for x in self.data])
    result = call_llm(text,instructions.replace('?', self.user), schema)
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
  action.run()
  action.print()
