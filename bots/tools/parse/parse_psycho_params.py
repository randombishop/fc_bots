from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_user


parse_user_instructions_template = """
#TASK:
You are @{{name}}, a bot programmed to psycho analyze a user.
Based on the provided context and instructions, who should we psycho analyze?
You must only extract the user parameter so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the context and instructions carefully to figure out the intended user.

#RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


def parse_psycho_params(input):
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
    'user': user_name,
    'user_fid': fid
  }


ParsePsychoParams = Tool(
  name="ParsePsychoParams",
  description="Set the parameters user and user_fid to run the psycho analysis tools.",
  func=parse_psycho_params
)