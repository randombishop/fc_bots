from bots.tools.b_plan.get_actions import GetActions
from bots.tools.b_plan.next_phase import NextPhase
from bots.tools.b_plan.select_action_for_channel import SelectActionForChannel
from bots.tools.b_plan.select_action_for_main_feed import SelectActionForMainFeed
from bots.tools.b_plan.select_action_from_conversation import SelectActionFromConversation
from bots.tools.b_plan.select_action_mode import SelectActionMode
from bots.tools.b_plan.select_channel import SelectChannel
from bots.tools.b_plan.should_continue import ShouldContinue



PLAN_TOOLS = [
  GetActions,
  NextPhase,
  SelectActionForChannel,
  SelectActionForMainFeed,
  SelectActionFromConversation,
  SelectActionMode,
  SelectChannel,
  ShouldContinue
]