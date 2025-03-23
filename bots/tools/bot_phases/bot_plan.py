from langchain.agents import Tool
from bots.tools.plan.get_actions import GetActions
from bots.tools.plan.select_action_from_conversation import SelectActionFromConversation
from bots.tools.plan.should_continue import ShouldContinue

def bot_plan(input):
  state = input.state
  if state.action is None:
    GetActions.invoke({'input': input})
    SelectActionFromConversation.invoke({'input': input})
  if state.conversation is not None and len(state.conversation) > 0:
    ShouldContinue.invoke({'input': input})
  return {
    'action': input.state.action,
    'should_continue': input.state.should_continue
  }


BotPlan = Tool(
  name="BotPlan",
  description="Bot plan phase",
  func=bot_plan
)