from bots.i_action_step import IActionStep
from bots.data.casts import get_casts_for_fid
from bots.utils.llms import call_llm
from bots.utils.read_params import read_user


parse_user_instructions_template = """
#INSTRUCTIONS
You are @{{name}}, a bot programmed to roast a user.
Based on the provided conversation, who should we roast?
Your goal is not to continue the conversation, you must only extract the user parameter from the conversation so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the conversation carefully to figure out the intended user.


#RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


instructions_template = """
#TASK
You are @{{name}}, a seasoned roast comedian known for your razor sharp wit and creative humor.
Your task is to roast @{{user_name}}.

#INSTRUCTIONS:
Analyze the posts provided from @{{user_name}} and craft a roast that is both hilarious and original.
Roast @{{user_name}} as hard as you can in one short but explosive tweet.
Cleverly highlight the quirky, absurd, or contradictory elements in the posts.
Use wordplay, irony, and playful sarcasm.
Maintain a humorous, light-hearted tone without resorting to unnecessarily mean-spirited personal attacks.
Be respectful, and do not use sexual, religious or political references.
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Output one single tweet in json format.

#RESPONSE FORMAT:
{
  "tweet": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "sentence1":{"type":"STRING"}
  }
}


class Roast(IActionStep):
    
  def get_cost(self):
    return 20
    
  def parse(self):
    parse_prompt = self.state.format_conversation()
    parse_instructions = self.state.format(parse_user_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_user_schema)
    parsed = {}
    fid, user_name = read_user(params, self.state.fid_origin, default_to_origin=True)
    parsed['fid'] = fid
    parsed['user_name'] = user_name
    self.state.action_params = parsed
    self.state.user = user_name

  def execute(self):
    fid = self.state.action_params['fid']
    if fid is None:
      raise Exception(f"No fid provided.")
    df = get_casts_for_fid(fid)
    if df is None or len(df) == 0:
      raise Exception(f"Not enough activity to roast.")
    data = list(df['text'])
    text = "\n".join([str(x) for x in data])
    instructions = self.state.format(instructions_template.replace('{{user_name}}', self.state.action_params['user_name']))
    result = call_llm(text, instructions, schema)
    cast = {'text': result['tweet']}
    casts = [cast]
    self.state.casts = casts
