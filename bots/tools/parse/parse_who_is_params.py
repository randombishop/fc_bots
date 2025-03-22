from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_user
from bots.data.bot_history import get_random_user_to_praise
from bots.data.users import get_fid


parse_user_instructions_template = """
#INSTRUCTIONS:
You are @{{name}}, a bot programmed to analyze a user profile and generate insights, plus a new avatar.
Based on the provided conversation, which user profile should we analyze?
Your goal is not to continue the conversation, you must only extract the user parameter from the conversation so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the conversation carefully to figure out the intended user.
If the request is targeted to a random user, set user to "*"

#RESPONSE FORMAT:
{
  "user": ...
}
"""


parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


def parse_who_is_params(input):
  state = input.state
  if state.user is not None:
    return {'log': 'User already set'}
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_user_instructions_template)
  params = call_llm(parse_prompt, parse_instructions, parse_user_schema)
  fid, user_name = read_user(params, state.fid_origin, default_to_origin=False)
  if user_name == '*' or user_name == '' or user_name is None:
    user_name = get_random_user_to_praise(state.id)
    fid = get_fid(user_name)
  state.user = user_name
  state.user_fid = fid
  return {
    'user': user_name,
    'user_fid': fid
  }


ParseWhoIsParams = Tool(
  name="ParseWhoIsParams",
  description="Parse the WhoIs action parameters",
  func=parse_who_is_params
)

