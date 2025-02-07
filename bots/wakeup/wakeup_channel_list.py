import random
from bots.i_wakeup_step import IWakeUpStep
from bots.data.bot_history import get_bot_channels


SAMPLE_SIZE = 10


class WakeUpChannelList(IWakeUpStep):
    
  def get(self, bot_character, bot_state):
    channels = get_bot_channels(bot_state.id)
    if len(channels)>SAMPLE_SIZE:
      channels = random.sample(channels, SAMPLE_SIZE)
      random.shuffle(channels)
    text = ''
    for s in channels:
      text += s['channel'] + "\n"
    return text
