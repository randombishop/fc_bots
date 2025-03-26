from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.llms import get_max_capactity
from bots.utils.read_params import read_category, read_channel, read_user, read_keyword, read_string
from bots.data.channels import get_channel_by_url


parse_instructions_template = """
#TASK:
You are @{{name}}, a bot programmed to select the best posts (=casts) in a social media platform.
You have access to an API that can pick the best post based on these parameters: 
category, channel, keyword, more_like_this, user, search, criteria.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* search: If the scope is not about a category, channel, keyword or user; then formulate a search phrase to search for posts and pick one.
* user: User names typically start with `@`, if the intent is to pick one post by a specific user, you can use the user parameter.
* criteria: Which criteria should be used to pick the best post? Can be any free text like 'beautiful', 'funniest', 'best', 'most informative'. Defaults to 'most interesting'.
Your goal is not to respond to the request at this point, you must only extract the parameters to call the API.

#CURRENT CHANNEL
{{channel}}

#RESPONSE FORMAT:
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

def parse_pick_params(input):
  if not input.state.is_responding():
    return {'log': 'Skipping parse_summary_params'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_prompt()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  state.channel_url = read_channel(params)
  state.channel = get_channel_by_url(state.channel_url)
  state.keyword = read_keyword(params)
  state.category = read_category(params)
  state.search = read_string(params, key='search', default=None, max_length=500)
  state.user_fid, state.user = read_user(params, fid_origin=state.fid_origin, default_to_origin=False)
  state.criteria = read_string(params, key='criteria', default='most interesting')
  state.max_rows = get_max_capactity()
  return {
    'channel_url': state.channel_url,
    'channel': state.channel,
    'keyword': state.keyword,
    'category': state.category,
    'search': state.search,
    'user': state.user,
    'user_fid': state.user_fid,
    'criteria': state.criteria,
    'max_rows': state.max_rows
  }
  

ParsePickParams = Tool(
  name="ParsePickParams",
  description="Parse the pick_cast action parameters",
  func=parse_pick_params
)
