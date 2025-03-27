from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.llms import get_max_capactity
from bots.utils.read_params import read_category, read_channel, read_user, read_keyword, read_string
from bots.data.channels import get_channel_by_url


parse_instructions_template = """
#TASK:
Your goal is to select the best posts (=casts) in a social media platform.
You have access to an API that can pick the best post based on these parameters: 
category, channel, keyword, more_like_this, user, search, criteria.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* search: If the scope is not about a category, channel, keyword or user; then formulate a search phrase to search for posts and pick one.
* user: User names typically start with `@`, if the intent is to pick one post by a specific user, you can use the user parameter.
* criteria: Which criteria should be used to pick the best post? Can be any free text like 'beautiful', 'funniest', 'best', 'most informative'. Defaults to 'most interesting'.
You must only extract the parameters to call the API.

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

def parse(input):
  state = input.state
  llm = input.llm
  parse_prompt = state.format_all()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  state.params['channel_url'] = read_channel(params)
  state.params['channel'] = get_channel_by_url(state.params['channel_url'])
  state.params['keyword'] = read_keyword(params)
  state.params['category'] = read_category(params)
  state.params['search'] = read_string(params, key='search', default=None, max_length=500)
  state.params['user_fid'], state.params['user'] = read_user(params, fid_origin=state.fid_origin, default_to_origin=False)
  state.params['criteria'] = read_string(params, key='criteria', default='most interesting')
  state.params['max_rows'] = get_max_capactity()
  return {
    'channel_url': state.params['channel_url'],
    'channel': state.params['channel'],
    'keyword': state.params['keyword'],
    'category': state.params['category'],
    'search': state.params['search'],
    'user': state.params['user'],
    'user_fid': state.params['user_fid'],
    'criteria': state.params['criteria'],
    'max_rows': state.params['max_rows']
  }
  

ParseCriteria = Tool(
  name="ParseCriteria",
  description="Set the parameters (one or more) channel_url, channel, keyword, category, search, user, user_fid, criteria and max_rows to be able to pick a cast.",
  func=parse
)
