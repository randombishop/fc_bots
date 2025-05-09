from bots.utils.llms2 import call_llm


instructions_template = """
#TASK
Your task is to shorten the provided text into a tweet no longer than 250 characters.

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


def shorten_text(text, style):
  prompt = text
  instructions = instructions_template.replace('{{style}}', str(style))
  result = call_llm('medium', prompt, instructions, schema)
  short = result['tweet']
  if len(short) > MAX_LENGTH:
    short = short[:MAX_LENGTH]+'...'
  return short


def cut_text(text):
  if text is None:
    return ''
  text_lines = text.split('\n')
  if len(text_lines) > 1:
    text = text_lines[0] + '...'
  if len(text) > MAX_LENGTH:
    text = text[:MAX_LENGTH]+'...'
  return text
