from bots.i_action_step import IActionStep
from bots.data.casts import get_casts_for_fid
from bots.utils.llms import call_llm
from bots.utils.read_params import read_user
from bots.utils.check_casts import check_casts



parse_user_instructions_template = """
You are @{{name}}, a bot programmed to roast a user.
Based on the provided conversation, who should we roast?
Your goal is not to continue the conversation, you must only extract the user parameter from the conversation so that we can call an API.
Users typically start with @, but not always.
If you're not sure, pick the last token that starts with a @.

RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


instructions = """
INSTRUCTIONS:
- The text above are extracts from ?.
- Based on their posts, roast them as hard as you can in one sentence.
- You are highly encouraged to be absurd, quote them and use random emojis as you make fun of them.
- Output the result in json format.
- Make sure you don't use " inside json strings. Avoid invalid json.

RESPONSE FORMAT:
{
  "sentence1": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "sentence1":{"type":"STRING"}
  }
}


class Roast(IActionStep):
  
  def set_input(self, input):
    params = call_llm(input, parse_user_instructions, parse_user_schema)
    self.input = input
    self.set_params(params)
    
  def set_params(self, params):
    self.fid, self.user_name = read_user(params, self.fid_origin, default_to_origin=True)

  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    df = get_casts_for_fid(self.fid)
    if df is None or len(df) == 0:
      raise Exception(f"Not enough activity to roast.")
    self.data = list(df['text'])
    return self.data
    
  def get_casts(self, intro=''):
    text = "\n".join([str(x) for x in self.data])
    result = call_llm(text, instructions.replace('?', self.user_name), schema)
    cast = {'text': result['sentence1']}
    casts = [cast]
    check_casts(casts)
    self.casts = casts
    return casts
