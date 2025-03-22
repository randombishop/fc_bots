from langchain.agents import Tool
from bots.tools.actions import get_action_config_tools
from bots.tools.combine import COMBINE_TOOLS


tool_map = {t.name: t for t in COMBINE_TOOLS}


def bot_combine(input):
  state = input.state
  selected_action = state.selected_action
  if selected_action is None:
    return {'log': 'No action selected'}
  tools = get_action_config_tools(selected_action, 'combine')
  if tools is None:
    return {'log': f'No tools configured for {selected_action}'}
  for t in tools:
    tool = tool_map[t]
    tool.invoke({'input': input})
  return {
    'tools': tools
  }


BotCombine = Tool(
  name="BotCombine",
  description="Bot combine phase",
  func=bot_combine
)