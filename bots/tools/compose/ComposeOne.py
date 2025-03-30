from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.format_cast import format_casts, extract_cast


instructions_template = """
You are @{{name}} bot

#YOUR BIO:
{{bio}}

#YOUR LORE:
{{lore}}

#YOUR STYLE:
{{style}}

#TASK:
Your goal is to respond to the user's instructions in one single tweet.
You can optionally embed an url or a post hash if it is relevant. 
When you want to embed an url or post, use the embed_url or embed_hash fields, don't include the link in the tweet itself.

#RESPONSE FORMAT:
{
  "tweet": "...",
  "embed_url": "...",
  "embed_hash": "..."
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "tweet":{"type":"STRING"},
    "embed_url":{"type":"STRING"},
    "embed_hash":{"type":"STRING"}
  }
}


def compose(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all()
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  c = extract_cast(result, state.posts_map)
  casts = [c] if c is not None else []
  formatted = format_casts(casts)
  return {
    'composed': True,
    'casts': formatted,
    'data_casts': casts
  }
  

ComposeOne = Tool(
  name="ComposeOne",
  description="Compose one cast to be posted by the bot.",
  func=compose
)
