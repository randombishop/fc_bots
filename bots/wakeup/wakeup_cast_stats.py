from bots.i_wakeup_step import IWakeUpStep
from bots.data.bot_history import get_bot_casts_stats
from bots.utils.format_cast import format_when


class WakeUpCastStats(IWakeUpStep):
    
  def get(self, bot_character, bot_state):
    stats = get_bot_casts_stats(bot_state.id)
    text = ''
    for s in stats:
      row = f"prompt='{s['action_prompt']}' | channel='{s['action_channel']}' | num_posts={s['num_posts']} |' avg_replies={s['avg_replies']:.1f} | avg_likes={s['avg_likes']:.1f} | avg_recasts={s['avg_recasts']:.1f} | last_post={format_when(s['last_post'])}\n"
      text += row
    return text
