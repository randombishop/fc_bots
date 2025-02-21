from bots.wakeup.wakeup_actions import WakeUpActions
from bots.wakeup.wakeup_actions_templates import WakeUpActionsTemplates
from bots.wakeup.wakeup_bio import WakeUpBio
from bots.wakeup.wakeup_channel_list import WakeUpChannelList
from bots.wakeup.wakeup_conversation import WakeUpConversation
from bots.wakeup.wakeup_lore import WakeUpLore
from bots.wakeup.wakeup_style import WakeUpStyle
from bots.wakeup.wakeup_time import WakeUpTime


WAKEUP_STEPS = {
  'actions': WakeUpActions,
  'actions_templates': WakeUpActionsTemplates,
  'bio': WakeUpBio,
  'channel_list': WakeUpChannelList,
  'conversation': WakeUpConversation,
  'lore': WakeUpLore,
  'style': WakeUpStyle,
  'time': WakeUpTime
}