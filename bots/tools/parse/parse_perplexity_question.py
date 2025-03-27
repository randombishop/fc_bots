from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_string


parse_instructions_template = """
#TASK:
Your goal is to forward a question to another AI that can search the web and generate an answer.
What question should we submit?
Extract or come up with an appropriate question.
You must only extract a question to call the next API.

#OUTPUT FORMAT:
{
  "question": "..."
}
"""


parse_schema = {
  "type":"OBJECT",
  "properties":{
    "question":{"type":"STRING"}
  }
}


def parse(input):
  state = input.state
  llm = input.llm
  parse_prompt = state.format_all()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  question = read_string(params, key='question', default=None, max_length=256)
  return {
    'question': question
  }
  
    
ParsePerplexityQuestion = Tool(
  name="ParsePerplexityQuestion",
  description="Set the parameter question to run the Perplexity tool.",
  metadata={
    'outputs': ['question']
  },
  func=parse
)
