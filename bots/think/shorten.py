from bots.i_think_step import IThinkStep
from bots.utils.llms import call_llm
from bots.utils.read_params import read_boolean
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


class Shorten(IThinkStep):
  
  def clean_text(self, text):
    if text is None:
      return None
    text = text.replace('$', '')
    text = re.sub(r'\[\d+\]', '', text)
    return text

  def shorten_text(self, text):
    print('<shorten_text>')
    prompt = self.state.format(prompt_template.replace('{{post}}', text))
    print(text)
    print('>>> >>> >>>')
    instructions = self.state.format(instructions_template)
    result = call_llm(prompt, instructions, schema)
    text = result['tweet']
    if len(text) > MAX_LENGTH:
      text = text[:MAX_LENGTH]+'...'
    print(text)
    print('</shorten_text>')
    return text

  def think(self):
    casts = self.state.casts
    for c in casts:
      if c['text'] is not None and len(c['text']) > MAX_LENGTH:
        c['text'] = self.shorten_text(c['text'])
      c['text'] = self.clean_text(c['text'])
