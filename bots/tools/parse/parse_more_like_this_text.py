from langchain.agents import Tool
from bots.utils.llms2 import call_llm


parse_instructions_template = """
#TASK:
Your goal is to forward a text to an API that will perform a more-like-this search.
What text should we submit?
Extract or come up with an appropriate text to be submitted to the more-like-this API.
You must only extract a text to call the more-like-this API.

#OUTPUT FORMAT:
{
  "text": "..."
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "text":{"type":"STRING"}
  }
}

def parse(input):
  if input.state.params['text'] is not None:
    return {'log': 'Text already set'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_all()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  text = params['text']
  state.params['text'] = text
  return {
    'text': state.params['text']
  }
  

ParseMoreLikeThisText = Tool(
  name="ParseMoreLikeThisText",
  description="Set parameter text to run the MoreLikeThis tools.",
  func=parse
)
