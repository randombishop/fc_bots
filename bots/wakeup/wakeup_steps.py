from bots.wakeup.wakeup_actions import WakeUpActions
from bots.wakeup.wakeup_bio import WakeUpBio
from bots.wakeup.wakeup_channel import WakeUpChannel
from bots.wakeup.wakeup_conversation import WakeUpConversation
from bots.wakeup.wakeup_lore import WakeUpLore
from bots.wakeup.wakeup_style import WakeUpStyle
from bots.wakeup.wakeup_time import WakeUpTime


WAKEUP_STEPS = {
  'actions': WakeUpActions,
  'bio': WakeUpBio,
  'channel': WakeUpChannel,
  'conversation': WakeUpConversation,
  'lore': WakeUpLore,
  'style': WakeUpStyle,
  'time': WakeUpTime
}