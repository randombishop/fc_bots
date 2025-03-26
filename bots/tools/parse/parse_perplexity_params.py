from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_string


parse_instructions_template = """
#TASK:
You are @{{name}} bot, a social media bot.
Your task is to forward a question to another AI that can search the web and generate an answer.
What question should we submit?
Extract or come up with an appropriate question.
Your goal is not to respond to the query at this point, you must only extract a question to call the next API.

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


def parse_perplexity_params(input):
  if input.state.question is not None:
    return {'log': 'Question already set'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_prompt()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  state.question = read_string(params, key='question', default=None, max_length=256)
  return {
    'question': state.question
  }
  
    
ParsePerplexityParams = Tool(
  name="ParsePerplexityParams",
  description="Set the parameter question to run the perplexity tools.",
  func=parse_perplexity_params
)
