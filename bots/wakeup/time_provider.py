from datetime import datetime
from bots.i_wakeup_step import IWakeUpStep


class WakeUpTime(IWakeUpStep):
    
  def get(self, bot_character, bot_state):    
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
  
  