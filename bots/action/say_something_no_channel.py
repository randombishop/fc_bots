from bots.i_action_step import IActionStep
from bots.utils.llms import call_llm


instructions_template = """
You are @{{name}}, a social media bot.
Your goal is to tweet something in the farcaster social network.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#TASK
You are provided with the recent trends, plus what you posted recently.
First, study the activity carefully and generate a short summary of the current trends in a couple of sentences.
Then, generate an original, creative and engaging tweet.
It can be a question, an affirmation, a joke or a haiku.
If something is at the intersection of the current activity and your character (bio and lore), it will be a great tweet idea.
Make sure your tweet is inline with the recent activity BUT DO NOT COPY OTHER POSTS.
Avoid repeating things you already posted.

#RESPONSE FORMAT
{
  "summary": "short summary of current activity."
  "tweet": "..."
}
"""


prompt_template = """
#WHAT PEOPLE ARE TALKING ABOUT
{{trending}}

#WHAT YOU RECENTLY POSTED
{{bot_casts_no_channel}}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "summary":{"type":"STRING"},
    "tweet":{"type":"STRING"}
  }
}


class SaySomethingNoChannel(IActionStep):
    
  def get_prepare_steps(self):
    return ['GetBotCastsNoChannel', 'GetTrending']
  
  def get_cost(self):
    return 20
    
  def auto_prompt(self):
    self.state.request = f'Say something in main feed'
    
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
