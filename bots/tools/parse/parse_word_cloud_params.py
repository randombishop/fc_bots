from langchain.agents import Tool
from bots.utils.call_llm import call_llm
from bots.utils.read_params import read_channel, read_user, read_string, read_category, read_keyword


parse_instructions_template = """
INSTRUCTIONS:
You are @{{name}}, a bot programmed to make a wordcloud based on posts (=casts) in a social media platform.
You have access to an API that can generate the wordcloud based on these parameters: category, channel, keyword, search, user.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* search: If the wordcloud is not about a category, channel, keyword or user; then formulate a search phrase to search for posts.
* user: User names typically start with `@`, if the intent is to make the wordcloud for a specific user, you can use the user parameter.
Your goal is not to continue the conversation, you must only extract the parameters to call the API.
You can use the conversation to guess the parameters, but focus on the request.
Your goal is to extract the parameters from the request.

#CURRENT CHANNEL
{{selected_channel}}

RESPONSE FORMAT:
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



def parse_word_cloud_params(input):
  state = input['state']
  llm = input['llm']
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  parsed = {}
  parsed['channel'] = read_channel(params)
  parsed['keyword'] = read_keyword(params)
  parsed['category'] = read_category(params)
  parsed['search'] = read_string(params, key='search', default=None, max_length=500)
  fid, user_name = read_user(params, fid_origin=state.fid_origin, default_to_origin=False)
  parsed['fid'] = fid
  parsed['user_name'] = user_name
  parsed['max_rows'] = 250
  state.action_params = parsed
  state.user = user_name
  state.user_fid = fid
  return {
    'action_params': state.action_params,
    'user': state.user,
    'user_fid': state.user_fid
  }
  
ParseWordCloudParams = Tool(
  name="parse_word_cloud_params",
  description="Parse the word cloud parameters",
  func=parse_word_cloud_params
)