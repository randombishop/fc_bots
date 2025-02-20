import random
from bots.i_wakeup_step import IWakeUpStep


class WakeUpStyle(IWakeUpStep):
    
  def get(self, bot_character, bot_state):    
    if bot_character['style'] is not None and len(bot_character['style']) > 0:
      style = bot_character['style']
      random.shuffle(style)
      return '\n'.join(style)      
    else:
      return ''
  
  