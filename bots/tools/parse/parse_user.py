from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_user


parse_user_instructions_template = """
#TASK:
You are @{{name}}, a bot programmed to praise a user.
Based on the provided conversation, who should we praise?
You must only extract the user parameter so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the context and instructions carefully to figure out the intended user.
If you decide to praise a random user, set user to "*"

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
  parse_prompt = state.format_prompt()
  parse_instructions = state.format(parse_user_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_user_schema)
  fid, user_name = read_user(params, state.fid_origin, default_to_origin=False)
  return {
    'user_fid': fid,
    'user': user_name
  }
  

ParseUser = Tool(
  name="ParseUser",
  description="Set the parameters user and user_fid to run the praise tools.",
  metadata={
    'outputs': ['user_fid', 'user']
  },
  func=parse
)
