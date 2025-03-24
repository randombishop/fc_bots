from langchain.agents import Tool
from bots.tools.bot_phases.bot_phase import run_phase
from bots.tools.fetch import FETCH_TOOLS


def bot_fetch(input):
  return run_phase(input, 'fetch', FETCH_TOOLS)
  

BotFetch = Tool(
  name="BotFetch",
  description="Bot fetch phase",
  func=bot_fetch
)