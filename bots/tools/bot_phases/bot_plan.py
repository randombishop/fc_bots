from langchain.agents import Tool
from bots.tools.plan.get_actions import GetActions
from bots.tools.plan.select_action_from_conversation import SelectActionFromConversation
from bots.tools.plan.should_continue import ShouldContinue

def bot_plan(input):
  GetActions.invoke({'input': input})
  SelectActionFromConversation.invoke({'input': input})
  ShouldContinue.invoke({'input': input})
  return {'selected_action': input.state.selected_action}


BotPlan = Tool(
  name="BotPlan",
  description="Bot plan phase",
  func=bot_plan
)