from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_string


parse_instructions_template = """
#TASK:
First, study the provided data and understand your instructions.
Before processing your instructions, you can pick the best post based on a particular criteria.
Which criteria should be used to pick a post? 
Can be any free text like 'beautiful', 'funniest', 'best', 'most informative'.
You must only extract the "criteria" parameter to call the API.

#RESPONSE FORMAT:
{
  "criteria": ...
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "criteria":{"type":"STRING"}
  }
}


def parse(input):
  state = input.state
  llm = input.llm
  parse_prompt = state.format_all()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  criteria = read_string(params, key='criteria', default='most interesting')
  return {
    'criteria': criteria
  }
  

ParseCriteria = Tool(
  name="ParseCriteria",
  description="Set the parameter `criteria` to be able to pick a post.",
  metadata={
    'outputs': ['criteria']
  },
  func=parse
)
