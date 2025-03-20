from bots.v2.tools.plan.next import Next
from bots.v2.tools.plan.select_action_for_channel import SelectActionForChannel
from bots.v2.tools.plan.select_action_for_main_feed import SelectActionForMainFeed
from bots.v2.tools.plan.select_action_from_conversation import SelectActionFromConversation
from bots.v2.tools.plan.select_action_mode import SelectActionMode
from bots.v2.tools.plan.select_channel import SelectChannel
from bots.v2.tools.plan.should_continue import ShouldContinue



PLAN_TOOLS = [
  Next,
  SelectActionForChannel,
  SelectActionForMainFeed,
  SelectActionFromConversation,
  SelectActionMode,
  SelectChannel,
  ShouldContinue
]