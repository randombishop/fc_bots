from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_category


parse_instructions_template = """
TASK:
First, study the provided data and understand your instructions.
Before processing your instructions, you can access data from the social media platform to prepare a good post.
You have access to an API that can pull data based on one of these categories:
'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
You must only extract the category parameter to call the API.


RESPONSE FORMAT:
{
  "category": "..."
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "category":{"type":"STRING"}
  }
}


def parse(input):
  state = input.state
  parse_prompt = state.format_all()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm('medium', parse_prompt, parse_instructions, parse_schema)
  category = read_category(params)
  return {
    'category': category
  }
  
desc = """Set the parameter category to run any category related tools.
Use ParseCategory whenever you find an explicit mention to a category in the instructions."""

ParseCategory = Tool(
  name="ParseCategory",
  description=desc,
  metadata={
    'outputs': ['category']
  },
  func=parse
)