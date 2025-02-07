from bots.i_wakeup_step import IWakeUpStep
from bots.data.bot_history import get_bot_recent_casts
from bots.utils.format_cast import shorten_text, format_when


class WakeUpRecentCasts(IWakeUpStep):
    
  def get(self, bot_character, bot_state):
    casts = get_bot_recent_casts(bot_state.id)
    text = ''
    for c in casts:
      row = '{\n'
      row += f"  prompt: {c['action_prompt']}\n"
      row += f"  post: {shorten_text(c['casted_text'])}\n"
      row += f"  channel: {c['action_channel']}\n"
      row += f"  when: {format_when(c['casted_at'])}\n"
      row += '}\n'
      text += row
    return text
