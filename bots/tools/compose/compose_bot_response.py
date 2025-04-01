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

#GOAL
{{request}}

#RESPONSE PLAN:
{{intended_response_plan}}

#TASK:
Your task is to respond to a user on a social media platform based on the provided context and instructions.
Output 1 response tweet or a thread of tweets up to 3 posts max in json format.
Prefer a response in 1 single tweet if possible, but you can use 2 or 3 tweets if really needed.
For your information, in the farcaster social media platform, posts are called casts.
You can optionally embed an url or a post hash if it is relevant. 
When you want to embed an url or post, use the embed_url or embed_hash fields, don't include the link or post id in the tweet field itself.
Output the result in json format.
Make sure you don't use " inside json strings. 
Avoid invalid json.

#RESPONSE FORMAT:
{
  "tweet1": "...",
  "embed_url1": "...",
  "embed_hash1": "...",
  "tweet2": "...",
  "embed_url2": "...",
  "embed_hash2": "...",
  "tweet3": "...",
  "embed_url3": "...",
  "embed_hash3": "...",
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "tweet1":{"type":"STRING"},
    "embed_url1":{"type":"STRING"},
    "embed_hash1":{"type":"STRING"},
    "tweet2":{"type":"STRING"},
    "embed_url2":{"type":"STRING"},
    "embed_hash2":{"type":"STRING"},
    "tweet3":{"type":"STRING"},
    "embed_url3":{"type":"STRING"},
    "embed_hash3":{"type":"STRING"}
  }
}


def compose(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all()
  instructions = state.format(instructions_template)
  intent = state.get('intent')
  result = call_llm(llm, prompt, instructions, schema)
  casts = []
  for i in range(1, 4):
    c = extract_cast(result, state.posts_map, i)
    if c is not None:
      casts.append(c)
  formatted = format_casts(casts)
  return {
    'composed': True,
    'casts': formatted,
    'data_casts': casts
  }
  

ComposeBotResponse = Tool(
  name="ComposeBotResponse",
  description="Compose one or multiple casts to be posted by the assistant.",
  func=compose
)
