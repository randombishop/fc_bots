import random
from bots.i_wakeup_step import IWakeUpStep

SAMPLE_SIZE = 5

class WakeUpLore(IWakeUpStep):
    
  def get(self, bot_character, bot_state):    
    if bot_character['lore'] is not None and len(bot_character['lore']) > 0:
      lore = bot_character['lore']
      if len(lore)>SAMPLE_SIZE:
        lore = random.sample(lore, SAMPLE_SIZE)
      random.shuffle(lore)
      return '\n'.join(lore)      
    else:
      return ''
  
  