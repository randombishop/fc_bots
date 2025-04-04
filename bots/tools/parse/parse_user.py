from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_user


parse_user_instructions_template = """
#TASK:
You are @{{name}}, a bot programmed to analyze user data and perform actions such as analyzing, praising, roasting, etc.
Based on the provided conversation, who should your tools target?
You must only extract the user parameter so that you can set the user parameter.
Users typically start with @, but not always.
If the request is about self or uses a pronoun, study the context and instructions carefully to figure out the intended user.

#RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


def parse(input):
  state = input.state
  llm = input.llm
  parse_prompt = state.format_all()
  parse_instructions = state.format(parse_user_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_user_schema)
  fid, user_name = read_user(params, fid_origin=state.get('fid_origin'), default_to_origin=False)
  if fid is None:
    user_name = None
  return {
    'user_fid': fid,
    'user': user_name
  }
  
desc= """"Set the parameters user and user_fid to run any user related tools. 
If it's a user related task like profile analysis, praise, roast, psycho analysis, etc, use ParseUser to set their id. 
Look out for particular user mention or a pronoun, if the instructions intent is directed to a person, select ParseUser to identify them."""

ParseUser = Tool(
  name="ParseUser",
  description=desc,
  metadata={
    'outputs': ['user_fid', 'user']
  },
  func=parse
)
