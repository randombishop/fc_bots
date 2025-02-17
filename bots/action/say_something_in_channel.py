from bots.i_action_step import IActionStep
from bots.utils.llms import call_llm


instructions_template = """
You are @{{name}}, a social media bot.
Your goal is to tweet something in the {{selected_channel}} channel.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#TASK
You are provided with the activity from channel {{selected_channel}}, plus what you posted recently there.
First, study the activity carefully and generate a short summary of the channel activity in a couple of sentences.
Then, generate an original, creative and engaging tweet.
It can be a question, an affirmation, a joke or a haiku.
If something is at the intersection of the channel activity and your character (bio and lore), it will be a great tweet idea.
Make sure your tweet is inline with the recent channel activity BUT DO NOT COPY OTHER POSTS.
Avoid repeating things you already posted.

#RESPONSE FORMAT
{
  "summary": "short summary of the channel activity."
  "tweet": "..."
}
"""


prompt_template = """
#WHAT PEOPLE ARE TALKING ABOUT
{{casts_in_channel}}

#WHAT YOU RECENTLY POSTED IN THE CHANNEL
{{bot_casts_in_channel}}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "summary":{"type":"STRING"},
    "tweet":{"type":"STRING"}
  }
}


class SaySomethingInChannel(IActionStep):
    
  def get_prepare_steps(self):
    return ['GetBotCastsInChannel', 'GetCastsInChannel']
  
  def get_cost(self):
    return 20
  
  def auto_prompt(self):
    self.state.request = f'Say something in channel /{self.state.selected_channel}'
    self.state.conversation = self.state.request
    
  def parse(self):
    pass

  def execute(self):
    prompt = self.state.format(prompt_template)
    instructions = self.state.format(instructions_template)
    result = call_llm(prompt, instructions, schema)
    if 'tweet' not in result or result['tweet'] is None or len(result['tweet']) < 2:
      raise Exception('Could not say something.')
    cast = {'text': result['tweet']}
    casts = [cast]
    summary = result['summary'] if 'summary' in result else ''
    self.state.casts = casts
    self.state.action_log += summary + '\n'
