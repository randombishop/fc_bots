from langchain.agents import Tool
from bots.tools.bot_phases.bot_phase import run_phase
from bots.tools.memorize import MEMORIZE_TOOLS


def bot_memorize(input):
  return run_phase(input, 'memorize', MEMORIZE_TOOLS)


BotMemorize = Tool(
  name="BotMemorize",
  description="Bot memorize phase",
  func=bot_memorize
)