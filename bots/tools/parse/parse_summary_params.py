from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_channel, read_keyword, read_category, read_string, read_user


parse_instructions_template = """
#CURRENT CHANNEL
{{channel}}

#INSTRUCTIONS
You are @{{name}}, a bot programmed to make summaries of posts (=casts) in a social media platform.
You have access to an API that can generate the summary based on these parameters: category, channel, keyword, search, user.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* search: If the summary is not about a category, channel, keyword or user; then formulate a search phrase to search for posts and summarize them.
* user: User names typically start with `@`, if the intent is to summarize posts by a specific user, you can use the user parameter.
Your goal is not to continue the conversation, you must only extract the parameters to call the API.
You can use the conversation to guess the parameters, but focus on the request.
Your goal is to extract the parameters from the request.

#RESPONSE FORMAT
{
  "category": "...",
  "channel": "...",
  "keyword": "...",
  "search": "...",
  "user": "..."
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "category":{"type":"STRING"},
    "channel":{"type":"STRING"},
    "keyword":{"type":"STRING"},
    "search":{"type":"STRING"},
    "user":{"type":"STRING"}
  }
}


def parse_summary_params(input):
  if not input.state.is_responding():
    return {'log': 'Skipping parse_summary_params'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  state.channel_url = read_channel(params)
  state.keyword = read_keyword(params)
  state.category = read_category(params)
  state.search = read_string(params, key='search', default=None, max_length=500)
  fid, user_name = read_user(params, fid_origin=state.fid_origin, default_to_origin=False)
  state.user = user_name
  state.user_fid = fid
  state.max_rows = 50
  return {
    'channel_url': state.channel_url,
    'keyword': state.keyword,
    'category': state.category,
    'search': state.search,
    'user': user_name,
    'user_fid': state.user_fid,
    'max_rows': state.max_rows
  }


ParseSummaryParams = Tool(
  name="ParseSummaryParams",
  func=parse_summary_params,
  description="Parse the summary parameters from the conversation"
)