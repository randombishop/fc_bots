from langchain.agents import Tool
from bots.tools.actions import get_action_config_tools
from bots.tools.fetch import FETCH_TOOLS


tool_map = {t.name: t for t in FETCH_TOOLS}


def bot_fetch(input):
  state = input.state
  selected_action = state.action
  if selected_action is None:
    return {'log': 'No action selected'}
  tools = get_action_config_tools(selected_action, 'fetch')
  if tools is None:
    return {'log': f'No tools configured for {selected_action}'}
  for t in tools:
    tool = tool_map[t]
    tool.invoke({'input': input})
  return {
    'tools': tools
  }


BotFetch = Tool(
  name="BotFetch",
  description="Bot fetch phase",
  func=bot_fetch
)