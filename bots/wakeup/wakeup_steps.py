from bots.wakeup.wakeup_actions import WakeUpActions
from bots.wakeup.wakeup_actions_templates import WakeUpActionsTemplates
from bots.wakeup.wakeup_bio import WakeUpBio
from bots.wakeup.wakeup_cast_stats import WakeUpCastStats
from bots.wakeup.wakeup_channel import WakeUpChannel
from bots.wakeup.wakeup_channel_list import WakeUpChannelList
from bots.wakeup.wakeup_conversation import WakeUpConversation
from bots.wakeup.wakeup_lore import WakeUpLore
from bots.wakeup.wakeup_recent_casts import WakeUpRecentCasts
from bots.wakeup.wakeup_style import WakeUpStyle
from bots.wakeup.wakeup_time import WakeUpTime
from bots.wakeup.wakeup_trending import WakeUpTrending


WAKEUP_STEPS = {
  'actions': WakeUpActions,
  'actions_templates': WakeUpActionsTemplates,
  'bio': WakeUpBio,
  'cast_stats': WakeUpCastStats,
  'channel': WakeUpChannel,
  'channel_list': WakeUpChannelList,
  'conversation': WakeUpConversation,
  'lore': WakeUpLore,
  'recent_casts': WakeUpRecentCasts,
  'style': WakeUpStyle,
  'time': WakeUpTime,
  'trending': WakeUpTrending
}