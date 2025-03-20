from langchain.agents import Tool
from bots.v2.call_llm import call_llm
from bots.utils.read_params import read_string


parse_instructions_template = """
You are @{{name}} bot, a social media bot.
Your task is to forward a question to another AI that can search the web and generate an answer.
What question should we submit?
Extract or come up with an appropriate question.
Your goal is not to continue the conversation, you must only extract a question to call the next API.
You can use the conversation as a context, but focus on the last request to come up with a good question.

OUTPUT FORMAT:
{
  "question": ""
}
"""


parse_schema = {
  "type":"OBJECT",
  "properties":{
    "question":{"type":"STRING"}
  }
}


def parse_perplexity_params(input):
  state = input['state']
  llm = input['llm']
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  parsed = {}
  parsed['question'] = read_string(params, key='question', default=None, max_length=256)
  state.action_params = parsed
  return {
    'action_params': state.action_params
  }
  
    
ParsePerplexityParams = Tool(
  name="parse_perplexity_params",
  description="Parse the perplexity action parameters",
  func=parse_perplexity_params
)
