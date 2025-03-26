from langchain.agents import Tool
from bots.tools.memorize import MEMORIZE_TOOLS


TOOL_MAP = {t.name: t for t in MEMORIZE_TOOLS}


ACTION_CONFIG = {
  'WhoIs': ['SaveUserProfile'],
  'Praise': ['SaveUserProfile']
}


def bot_memorize(input):
  action = input.state.action
  if action is None or action not in ACTION_CONFIG:
    return {'log': 'Memorize tools are not configured for this action'}
  tool_names = ACTION_CONFIG[action]
  tools = [TOOL_MAP[t] for t in tool_names]
  for t in tools:
    t.invoke({'input': input})
  return {
    'memorize_tools': tools
  }


BotMemorize = Tool(
  name="BotMemorize",
  description="Bot memorize phase",
  func=bot_memorize
)