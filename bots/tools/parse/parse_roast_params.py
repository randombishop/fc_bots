from langchain.agents import Tool
from bots.utils.llms2 import call_llm
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

def parse_roast_params(input):
  if input.state.user is not None:
    return {'log': 'User already set'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_user_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_user_schema)
  fid, user_name = read_user(params, state.fid_origin, default_to_origin=True)
  state.user = user_name
  state.user_fid = fid
  return {
    'user': user_name,
    'user_fid': fid
  }


ParseRoastParams = Tool(
  name="ParseRoastParams",
  description="Parse the roast action parameters",
  func=parse_roast_params
)
