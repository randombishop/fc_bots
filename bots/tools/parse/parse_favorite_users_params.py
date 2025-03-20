from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_user



parse_user_instructions_template = """
INSTRUCTIONS:
You are @{{name}}, a bot programmed to find the favorite accounts of a user.
Based on the provided conversation and request, who should we pull the favorite accounts for?
Your goal is not to continue the conversation, you must only extract the user parameter from the request so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the conversation carefully to figure out the intended user.

RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


def parse_favorite_users(input):
  state = input.state
  llm = input.llm
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_user_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_user_schema)
  parsed = {}
  fid, user_name = read_user(params, state.fid_origin, default_to_origin=True)
  parsed['fid'] = fid
  parsed['user_name'] = user_name
  state.action_params = parsed
  state.user = user_name
  state.user_fid = fid
  return {
    'action_params': state.action_params,
    'user': state.user,
    'user_fid': state.user_fid
  }


ParseFavoriteUsersParams = Tool(
  name="parse_favorite_users_params",
  description="Parse the favorite users action parameters",
  func=parse_favorite_users
)
