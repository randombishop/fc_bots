from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.data.casts import get_more_like_this


parse_instructions_template = """
You are @{{name}}, a social media bot.
Your task is to forward a text to an API that will perform a more-like-this search.
What text should we submit?
Extract or come up with an appropriate text to be submitted to the more-like-this API.
Your goal is not to continue the conversation, you must only extract a text to call the next API.
You can use the conversation for more context if needed, but focus on the request to find out the intent of the last user.

OUTPUT FORMAT:
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

def parse_more_like_this_params(input):
  if input.state.text is not None:
    return {'log': 'Text already set'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_conversation()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  text = params['text']
  if text is None or len(text) < 5:
    raise Exception("This action requires some text to find similar posts.")
  state.text = text
  return {
    'text': text
  }
  

ParseMoreLikeThisParams = Tool(
  name="ParseMoreLikeThisParams",
  description="Parse the more like this action parameters",
  func=parse_more_like_this_params
)
