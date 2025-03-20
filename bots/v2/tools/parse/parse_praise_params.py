from langchain.agents import Tool
from bots.v2.call_llm import call_llm
from bots.utils.read_params import read_user
from bots.data.bot_history import get_random_user_to_praise
from bots.data.users import get_fid


parse_user_instructions_template = """
#INSTRUCTIONS:
You are @{{name}}, a bot programmed to praise a user.
Based on the provided conversation, who should we praise?
Your goal is not to continue the conversation, you must only extract the user parameter from the conversation so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the conversation carefully to figure out the intended user.
If the request is to praise a random user, set user to "*"

#RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


def parse_praise_params(input):
  state = input['state']
  llm = input['llm']
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_user_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_user_schema)
  parsed = {}
  fid, user_name = read_user(params, state.fid_origin, default_to_origin=False)
  if user_name == '*' or user_name == '' or user_name is None:
    user_name = get_random_user_to_praise(state.id)
    fid = get_fid(user_name)
  parsed['fid'] = fid
  parsed['user_name'] = user_name
  state.action_params = parsed
  state.user_fid = fid
  state.user = user_name
  return {
    'action_params': state.action_params,
    'user_fid': state.user_fid,
    'user': state.user
  }
  

ParsePraiseParams = Tool(
  name="parse_praise_params",
  description="Parse the praise action parameters",
  func=parse_praise_params
)
