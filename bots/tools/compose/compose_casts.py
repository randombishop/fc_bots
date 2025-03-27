from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.check_links import check_link_data
from bots.utils.format_cast import format_casts


instructions_template = """
#TASK:
You are @{{name}} bot
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


def extract_cast(result, index, posts_map):
  if f'tweet{index}' not in result:
    return None
  c = {'text': result[f'tweet{index}']}
  if f'embed_url{index}' in result:
    c['embeds'] = [result[f'embed_url{index}']]
    c['embeds_description'] = 'link'
  elif f'embed_hash{index}' in result:
    link = check_link_data({'id': result[f'embed_hash{index}']}, posts_map)
    if link is not None:
      c['embeds'] = [{'fid': link['fid'], 'user_name': link['user_name'], 'hash': link['hash']}],
      c['embeds_description'] = link['text']
      c['embeds_warpcast'] = f"https://warpcast.com/{link['user_name']}/{link['hash'][:10]}"
  return c


def compose_casts(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all()
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  casts = []
  for i in range(1, 4):
    c = extract_cast(result, i, state.posts_map)
    if c is not None:
      casts.append(c)
  formatted = format_casts(casts)
  return {
    'casts': formatted,
    'data_casts': casts
  }
  

ComposeCasts = Tool(
  name="ComposeCasts",
  description="Compose casts to be posted",
  func=compose_casts
)
