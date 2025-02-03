import random
from bots.i_wakeup_step import IWakeUpStep

SAMPLE_SIZE = 10

class WakeUpStyle(IWakeUpStep):
    
  def get(self, bot_character, bot_state):    
    if bot_character['style'] is not None and len(bot_character['style']) > 0:
      style = bot_character['style']
      if len(style)>SAMPLE_SIZE:
        style = random.sample(style, SAMPLE_SIZE)
      random.shuffle(style)
      return '\n'.join(style)      
    else:
      return ''
  
  