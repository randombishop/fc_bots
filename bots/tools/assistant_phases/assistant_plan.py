from langchain.agents import Tool
from bots.tools.plan.get_actions import GetActions
from bots.tools.plan.select_action_from_instructions import SelectActionFromInstructions


def assistant_plan(input):
  state = input.state
  if state.action is None:
    GetActions.invoke({'input': input})
    SelectActionFromInstructions.invoke({'input': input})
  if state.action is not None:
    pass
  return {
    'action': input.state.action,
    'action_reasoning': input.state.action_reasoning
  }


AssistantPlan = Tool(
  name="AssistantPlan",
  description="Assistant plan phase",
  func=assistant_plan
)