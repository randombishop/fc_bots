from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_keyword, read_string


instructions_template = """
#TASK
First, study the provided context and understand your instructions.
Based on the provided context and instructions, which keyword should we look at? 
You must only extract the keyword to be able to use your next tools.
Do not use an abbreviation for the keyword, it has to be at least 4 characters long.
The keyword should be a single word, not a phrase.
Output your response in the following json format.

#RESPONSE FORMAT
{
  "keyword": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "keyword":{"type":"STRING"}
  }
}


def parse(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all()
  instructions = state.format(instructions_template)
  params = call_llm(llm, prompt, instructions, schema)
  keyword = read_keyword(params)
  return {
    'keyword': keyword
  }

desc = """Set parameter keyword to pull relevant posts.
Use ParseKeyword when you require searching for posts with a single keyword."""

ParseKeyword = Tool(
  name="ParseKeyword",
  description=desc,
  metadata={
    'outputs': ['keyword']
  },
  func=parse
)