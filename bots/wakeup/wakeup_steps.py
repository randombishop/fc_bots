from bots.wakeup.wakeup_actions import WakeUpActions
from bots.wakeup.wakeup_bio import WakeUpBio
from bots.wakeup.wakeup_cast_stats import WakeUpCastStats
from bots.wakeup.wakeup_channel import WakeUpChannel
from bots.wakeup.wakeup_channel_summaries import WakeUpChannelSummaries
from bots.wakeup.wakeup_conversation import WakeUpConversation
from bots.wakeup.wakeup_lore import WakeUpLore
from bots.wakeup.wakeup_style import WakeUpStyle
from bots.wakeup.wakeup_time import WakeUpTime
from bots.wakeup.wakeup_trending import WakeUpTrending


WAKEUP_STEPS = {
  'actions': WakeUpActions,
  'bio': WakeUpBio,
  'cast_stats': WakeUpCastStats,
  'channel': WakeUpChannel,
  'channel_summaries': WakeUpChannelSummaries,
  'conversation': WakeUpConversation,
  'lore': WakeUpLore,
  'style': WakeUpStyle,
  'time': WakeUpTime,
  'trending': WakeUpTrending
}