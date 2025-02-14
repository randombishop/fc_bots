from bots.i_prepare_step import IPrepareStep
from bots.data.bot_history import get_bot_recent_casts_in_channel
from bots.utils.format_cast import shorten_text, format_when


class GetBotCastsInChannel(IPrepareStep):
    
  def prepare(self):
    casts = get_bot_recent_casts_in_channel(self.state.id, self.state.channel)
    text = ''
    for c in casts:
      row = '{\n'
      row += f"  prompt: {c['action_prompt']}\n"
      row += f"  post: {shorten_text(c['casted_text'])}\n"
      row += f"  when: {format_when(c['casted_at'])}\n"
      row += '}\n'
      text += row
    self.state.bot_casts_in_channel = text
