from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_keyword, read_string


instructions_template = """
#TASK
First, study the provided data and understand your instructions.
Based on the provided context and instructions, extract a search phrase to lookup social media posts. 
The search algorithm uses semantic search so the search phrase can be any short phrase.
Make the search phrase specific to the instructions intent but keep it short.
Output your response in the following json format.
Avoid quotes and invalid json in the search string.

#RESPONSE FORMAT
{
  "search": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "search":{"type":"STRING"}
  }
}


def parse(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all()
  instructions = state.format(instructions_template)
  params = call_llm(llm, prompt, instructions, schema)
  search = read_string(params, key='search', max_length=500)
  return {
    'search': search
  }

desc = """Set the search parameter to pull relevant posts.
Use ParseSearchPhrase when you need to search for posts using semantic search."""

ParseSearchPhrase = Tool(
  name="ParseSearchPhrase",
  description=desc,
  metadata={
    'outputs': ['search']
  },
  func=parse
)