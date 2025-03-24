from langchain.agents import Tool
from bots.tools.bot_phases.bot_phase import run_phase
from bots.tools.prepare import PREPARE_TOOLS


def bot_prepare(input):
  return run_phase(input, 'prepare', PREPARE_TOOLS)


BotPrepare = Tool(
  name="BotPrepare",
  description="Bot prepare phase",
  func=bot_prepare
)