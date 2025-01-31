from bots.wakeup.wakeup_bio import WakeUpBio
from bots.wakeup.wakeup_lore import WakeUpLore
from bots.wakeup.wakeup_time import WakeUpTime
from bots.wakeup.wakeup_channel import WakeUpChannel
from bots.wakeup.wakeup_conversation import WakeUpConversation


WAKEUP_STEPS = {
  'bio': WakeUpBio,
  'lore': WakeUpLore,
  'time': WakeUpTime,
  'channel': WakeUpChannel,
  'conversation': WakeUpConversation
}