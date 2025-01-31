from bots.i_wakeup_step import IWakeUpStep
from bots.data.channels import get_channel_by_url

class WakeUpChannel(IWakeUpStep):
    
  def get(self, bot_character, bot_state):
    text = ''
    if bot_state.root_parent_url is not None:
      channel_id = get_channel_by_url(bot_state.root_parent_url)
      if channel_id is not None:
        text += '/'+channel_id
    return text
  
  