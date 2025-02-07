from bots.i_wakeup_step import IWakeUpStep
from bots.data.bot_history import get_bot_casts_stats
from bots.utils.format_cast import format_when


class WakeUpCastStats(IWakeUpStep):
    
  def get(self, bot_character, bot_state):
    stats = get_bot_casts_stats(bot_state.id)
    text = ''
    for s in stats:
      row = '{\n'
      row += f"  prompt: {s['action_prompt']}\n"
      row += f"  channel: {s['action_channel']}\n"
      row += f"  num_posts: {s['num_posts']}\n"
      row += f"  avg_replies: {s['avg_replies']:.1f}\n"
      row += f"  avg_likes: {s['avg_likes']:.1f}\n"
      row += f"  avg_recasts: {s['avg_recasts']:.1f}\n"
      row += '}\n'
      text += row
    return text