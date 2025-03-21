from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.llms import get_max_capactity
from bots.utils.read_params import read_category, read_channel, read_user, read_keyword, read_string


parse_instructions_template = """
INSTRUCTIONS:
You are @{{name}}, a bot programmed to select the best posts (=casts) in a social media platform.
You have access to an API that can pick the best post based on these parameters: 
category, channel, keyword, more_like_this, user, search, criteria.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* search: If the scope is not about a category, channel, keyword or user; then formulate a search phrase to search for posts and pick one.
* user: User names typically start with `@`, if the intent is to pick one post by a specific user, you can use the user parameter.
* criteria: Which criteria should be used to pick the best post? Can be any free text like 'beautiful', 'funniest', 'best', 'most informative'. Defaults to 'most interesting'.
Your goal is not to continue the conversation, you must only extract the parameters to call the API.
You can use the conversation to guess the parameters, but focus on the request.
Your goal is to extract the parameters from the request.

#CURRENT CHANNEL
{{selected_channel}}

RESPONSE FORMAT:
{
  "category": ...,
  "channel": ...,
  "keyword": "...",
  "search": "...",
  "user": "..."
  "criteria": ...
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "category":{"type":"STRING"},
    "channel":{"type":"STRING"},
    "keyword":{"type":"STRING"},
    "search":{"type":"STRING"},
    "user":{"type":"STRING"},
    "criteria":{"type":"STRING"}
  }
}

def parse_pick_cast_params(input):
  state = input.state
  llm = input.llm
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  parsed = {}
  parsed['channel'] = read_channel(params)
  parsed['keyword'] = read_keyword(params)
  parsed['category'] = read_category(params)
  parsed['search'] = read_string(params, key='search', default=None, max_length=500)
  _, parsed['user_name'] = read_user(params, fid_origin=state.fid_origin, default_to_origin=False)
  parsed['criteria'] = read_string(params, key='criteria', default='most interesting')
  parsed['max_rows'] = get_max_capactity()
  state.action_params = parsed
  return {
    'action_params': state.action_params
  }
  

ParsePickCastParams = Tool(
  name="parse_pick_cast_params",
  description="Parse the pick_cast action parameters",
  func=parse_pick_cast_params
)
