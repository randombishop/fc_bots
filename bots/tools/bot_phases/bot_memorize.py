from langchain.agents import Tool
from bots.tools.actions import get_action_config_tools
from bots.tools.memorize import MEMORIZE_TOOLS


tool_map = {t.name: t for t in MEMORIZE_TOOLS}


def bot_memorize(input):
  state = input.state
  selected_action = state.action
  if selected_action is None:
    return {'log': 'No action selected'}
  tools = get_action_config_tools(selected_action, 'memorize')
  if tools is None:
    return {'log': f'No tools configured for {selected_action}'}
  for t in tools:
    tool = tool_map[t]
    tool.invoke({'input': input})
  return {
    'tools': tools
  }


BotMemorize = Tool(
  name="BotMemorize",
  description="Bot memorize phase",
  func=bot_memorize
)