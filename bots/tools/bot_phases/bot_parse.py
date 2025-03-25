from langchain.agents import Tool
from bots.tools.bot_phases.bot_phase import run_phase
from bots.tools.parse import PARSE_TOOLS


def bot_parse(input):
  state = input.state
  run_phase(input, 'parse', PARSE_TOOLS)
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