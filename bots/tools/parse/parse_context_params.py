from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_keyword, read_category, read_string


instructions_template = """
You are @{{name}}, a social media bot.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#CURRENT CHANNEL
{{root_parent_url}}

#CURRENT TIME
{{time}}

#TASK
Before responding to the user, you can access data from the social media platform to come up with a better response and reference relevant posts.
You have access to an API that can pull data based on these parameters: category, keyword, search.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* keyword: Can be any single keyword, minimum 4 characters, abbreviations are not allowed.
* search: Can be any search phrase to search for posts.
Your goal is not to continue the conversation, you must only come up with interesting parameters to call the API.
Your goal is to propose parameters to gain access to more data before responding.

#RESPONSE FORMAT
{
  "category": "...",
  "keyword": "...",
  "search": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "category":{"type":"STRING"},
    "keyword":{"type":"STRING"},
    "search":{"type":"STRING"}
  }
}


def parse_context_params(input):
  state = input.state
  llm = input.llm
  if not state.should_continue:
    return {'log': 'Not fetching data because should_continue is false'}
  prompt = state.format_conversation()
  instructions = state.format(instructions_template)
  params = call_llm(llm, prompt, instructions, schema)
  state.keyword = read_keyword(params)
  state.category = read_category(params)
  state.search = read_string(params, key='search', default=None, max_length=500)
  state.max_rows = 25
  return {
    'keyword': state.keyword,
    'category': state.category, 
    'search': state.search,
    'max_rows': state.max_rows
  }


ParseContextParams = Tool(
  name="ParseContextParams",
  func=parse_context_params,
  description="Parse parameters to build up context"
)