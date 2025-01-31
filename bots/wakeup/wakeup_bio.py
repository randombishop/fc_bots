import random
from bots.i_wakeup_step import IWakeUpStep

SAMPLE_SIZE = 5

class WakeUpBio(IWakeUpStep):
    
  def get(self, bot_character, bot_state):    
    if bot_character['bio'] is not None and len(bot_character['bio']) > 0:
      bio = bot_character['bio']
      if len(bio)>SAMPLE_SIZE:
        bio = random.sample(bio, SAMPLE_SIZE)
      random.shuffle(bio)
      return '\n'.join(bio)      
    else:
      return ''
  
  