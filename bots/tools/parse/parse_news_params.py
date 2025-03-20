from langchain.agents import Tool
from bots.utils.call_llm import call_llm
from bots.utils.read_params import read_string


parse_instructions_template = """
You are @{{name}} bot, a social media bot.
Your task is to forward a search query to a news API and get an interesting story.
What search query should we submit?
Extract or come up with an appropriate search query.
Your goal is not to continue the conversation, you must only extract a search query to call the next API.
You can use the conversation as a context for the request, but focus on the last request to come up with a good search query.

OUTPUT FORMAT:
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
  state = input['state']
  llm = input['llm']
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  parsed = {}
  parsed['search'] = read_string(params, key='search', default=None, max_length=256)
  state.action_params = parsed
  return {
    'action_params': state.action_params
  }
  
  
ParseNewsParams = Tool(
  name="parse_news_params",
  description="Parse the news action parameters",
  func=parse_news_params
)
