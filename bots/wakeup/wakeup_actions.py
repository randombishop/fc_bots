import random
from bots.i_wakeup_step import IWakeUpStep
from bots.action.action_steps import DESCRIPTIONS

RANDOMIZE = True

class WakeUpActions(IWakeUpStep):
    
  def get(self, bot_character, bot_state):    
    if bot_character['action_steps'] is not None and len(bot_character['action_steps']) > 0:
      actions = bot_character['action_steps']
      if RANDOMIZE:
        random.shuffle(actions)
      ans = ''
      for action in actions:
        ans += f'{action}: {DESCRIPTIONS[action]}\n'
      return ans
    else:
      return ''
  
  