from langchain.agents import Tool
from bots.utils.call_llm import call_llm
import re


prompt_template = """
#CONVERSATION
{{conversation}}

#POST
{{post}}

#TASK
Your task is to shorten the post into a tweet no longer than 250 characters.
Output json in this format: {"tweet": "short version of the post"})
"""


instructions_template = """
You are @{{name}} bot, a social media bot.
Your task is to shorten the provided post into a tweet no longer than 250 characters.

#YOUR STYLE
{{style}}

INSTRUCTIONS:
Rewrite the post into a shorter version, max 250 characters.
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.

OUTPUT FORMAT:
{
  "tweet": "string"
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "tweet":{"type":"STRING"}
  }
}


MAX_LENGTH = 275


def clean_text(text):
  if text is None:
    return None
  text = text.replace('$', '')
  text = text.replace('tweet', 'cast')
  text = re.sub(r'\[\d+\]', '', text)
  text = re.sub(r'[\(\[][a-f0-9]{6}[\)\]]', '', text)
  if len(text) > 2:
    if text[0]=='"':
      text = text[1:]
    if text[-1]=='"':
      text = text[:-1]
  return text

def shorten_text(state, llm, text):
  prompt = state.format(prompt_template.replace('{{post}}', text))
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  short = result['tweet']
  if len(short) > MAX_LENGTH:
    short = short[:MAX_LENGTH]+'...'
  return short

def shorten(input):
  state = input['state']
  llm = input['llm']
  casts = state.casts
  for c in casts:
    if c['text'] is not None and len(c['text']) > MAX_LENGTH:
      c['text'] = shorten_text(state, llm, c['text'])
    c['text'] = clean_text(c['text'])
  return {
    'casts': casts
  }


Shorten = Tool(
  name="Shorten",
  description="Shorten the posts into casts no longer than 250 characters",
  func=shorten
)
