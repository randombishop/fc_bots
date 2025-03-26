from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_string


parse_instructions_template = """
#TASK:
You are @{{name}} bot, a social media bot.
Your task is to forward a search query to a news API and get an interesting story.
What search query should we submit?
Extract or come up with an appropriate search query.
Your goal is not to respond to the query at this point, you must only extract a search query to call the next API.

#OUTPUT FORMAT:
{
  "search": "..."
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "search":{"type":"STRING"}
  }
}


def parse_news_params(input):
  if input.state.search is not None:
    return {'log': 'Search already set'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_prompt()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  state.search = read_string(params, key='search', default=None, max_length=256)
  return {
    'search': state.search
  }
  
  
ParseNewsParams = Tool(
  name="ParseNewsParams",
  description="Parse the news action parameters",
  func=parse_news_params
)
