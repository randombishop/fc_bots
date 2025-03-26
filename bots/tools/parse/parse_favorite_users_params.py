from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_user



parse_user_instructions_template = """
#TASK:
You are @{{name}}, a bot programmed to find the favorite accounts of a user.
Based on the provided instructions, who should we pull the favorite accounts for?
Your goal is not to continue the conversation, you must only extract the user parameter so that we can call an API.
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


def parse_favorite_users(input):
  if input.state.user is not None:
    return {'log': 'User already set'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_prompt()
  parse_instructions = state.format(parse_user_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_user_schema)
  fid, user_name = read_user(params, state.fid_origin, default_to_origin=True)
  state.user = user_name
  state.user_fid = fid
  return {
    'user': state.user,
    'user_fid': state.user_fid
  }


ParseFavoriteUsersParams = Tool(
  name="ParseFavoriteUsersParams",
  description="Set parameters user and user_fid to run the favorite users tools.",
  func=parse_favorite_users
)
