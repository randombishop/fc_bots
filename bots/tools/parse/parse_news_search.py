from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_string


parse_instructions_template = """
#TASK:
Your goal is to forward a search query to a news API and get an interesting story.
What search query should we submit?
Extract or come up with an appropriate search query.
You must only extract a search query to call the next API.

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


def parse(input):
  state = input.state
  llm = input.llm
  parse_prompt = state.format_all()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  search = read_string(params, key='search', default=None, max_length=256)
  return {
    'search': search
  }
  
desc = """Set the parameter search. Use ParseNewsSearch when you need to do a yahoo news search."""

ParseNewsSearch = Tool(
  name="ParseNewsSearch",
  description=desc,
  metadata={
    'outputs': ['search']
  },
  func=parse
)
