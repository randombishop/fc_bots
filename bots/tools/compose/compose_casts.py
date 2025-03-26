from langchain.agents import Tool
from bots.utils.llms2 import call_llm


instructions_template = """
You are @{{name}} bot

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#INSTRUCTIONS:
{{instructions}}
Output 1 to 3 posts max in json format.
You are highly encouraged to embed the urls that you prepared before (from the first candidate cast) 
You can also embed other posts by referencing their hash when applicable.
Prefer a response in 1 single tweet if possible, but you can use 2 or 3 tweets if really needed.

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


def compose_casts(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all_available_data()
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  return result
  

ComposeCasts = Tool(
  name="ComposeCasts",
  description="Compose casts to be posted",
  func=compose_casts
)
