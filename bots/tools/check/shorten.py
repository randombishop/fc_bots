from langchain.agents import Tool
from bots.utils.llms2 import call_llm
import re
from bots.utils.format_cast import format_casts

prompt_template = """
#REQUEST
{{request}}

#POST
{{post}}

#TASK
Your task is to shorten the post into a tweet no longer than 250 characters.
Output json in this format: {"tweet": "short version of the post"})
"""


instructions_template = """
#TASK
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

def shorten_text(state, text):
  prompt = state.format(prompt_template.replace('{{post}}', text))
  instructions = state.format(instructions_template)
  result = call_llm('medium', prompt, instructions, schema)
  short = result['tweet']
  if len(short) > MAX_LENGTH:
    short = short[:MAX_LENGTH]+'...'
  return short

def shorten(input):
  state = input.state
  casts = state.get('data_casts')
  log = []
  for c in casts:
    original = c['text']
    if original is not None and len(original) > MAX_LENGTH:
      c['text'] = shorten_text(state, original)
    c['text'] = clean_text(c['text'])
    if original != c['text']:
      log.append(f'{original}\n>>>\n{c["text"]}')
  if len(log) == 0:
    return {'shorten': 'No change'}
  else:
    formatted = format_casts(casts)
    return {
      'casts': formatted,
      'data_casts': casts,
      'log': log
    }


Shorten = Tool(
  name="Shorten",
  description="Shorten the posts into casts no longer than 250 characters",
  metadata={
    'inputs': ['data_casts']
  },
  func=shorten
)
