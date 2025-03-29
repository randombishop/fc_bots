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
Your goal is to generate social media post or thread based on the provided context and instructions.
Output 1 to 3 posts max in json format.
You can optionally embed an url or a post hash if it is relevant. 
When you want to embed an url or post, use the embed_url or embed_hash fields, don't include the link in the tweet itself.
Prefer a response in 1 single tweet if possible, but you can use 2 or 3 tweets if really needed.
If the main task specifies posting one post, keep it one single tweet.
If the main task specifies posting a thread, generate 2 or 3 tweets. 
Avoid phrasing your post like previous similar ones, be creative.

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
  result = call_llm(llm, prompt, instructions, schema)
  casts = []
  for i in range(1, 4):
    c = extract_cast(result, state.posts_map, i)
    if c is not None:
      casts.append(c)
  formatted = format_casts(casts)
  state.composed = True
  return {
    'casts': formatted,
    'data_casts': casts
  }
  

ComposeMulti = Tool(
  name="ComposeMulti",
  description="Compose one or multiple casts to be posted by the bot.",
  func=compose
)
