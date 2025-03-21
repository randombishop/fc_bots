from bots.tools.plan.get_actions import GetActions
from bots.tools.plan.select_action_for_channel import SelectActionForChannel
from bots.tools.plan.select_action_for_main_feed import SelectActionForMainFeed
from bots.tools.plan.select_action_from_conversation import SelectActionFromConversation
from bots.tools.plan.select_action_mode import SelectActionMode
from bots.tools.plan.select_channel import SelectChannel
from bots.tools.plan.should_continue import ShouldContinue



PLAN_TOOLS = [
  GetActions,
  SelectActionForChannel,
  SelectActionForMainFeed,
  SelectActionFromConversation,
  SelectActionMode,
  SelectChannel,
  ShouldContinue
]