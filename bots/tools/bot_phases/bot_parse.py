from langchain.agents import Tool
from bots.tools.actions import get_action_config_tools
from bots.tools.parse import PARSE_TOOLS


tool_map = {t.name: t for t in PARSE_TOOLS}


def bot_parse(input):
  state = input.state
  selected_action = state.action
  if selected_action is None:
    return {'log': 'No action selected'}
  tools = get_action_config_tools(selected_action, 'parse')
  if tools is None:
    return {'log': f'No tools configured for {selected_action}'}
  for t in tools:
    tool = tool_map[t]
    tool.invoke({'input': input})
  return {
    'user': state.user,
    'user_fid': state.user_fid,
    'channel_url': state.channel_url,
    'keyword': state.keyword,
    'category': state.category,
    'search': state.search,
    'text': state.text,
    'question': state.question,
    'criteria': state.criteria,
    'max_rows': state.max_rows
  }


BotParse = Tool(
  name="BotParse",
  description="Bot parse phase",
  func=bot_parse
)