from bots.i_wakeup_step import IWakeUpStep
from bots.data.bot_history import get_channel_summaries
from bots.utils.format_cast import format_when


class WakeUpChannelSummaries(IWakeUpStep):
    
  def get(self, bot_character, bot_state):
    summaries = get_channel_summaries(bot_state.id)
    text = ''
    for s in summaries:
      row = f"Channel /{s['channel']} summarized {format_when(s['timestamp'])}: {s['text']}\n"
      text += row
    return text
