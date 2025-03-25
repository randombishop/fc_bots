from langchain.agents import Tool
from bots.tools.compose import COMPOSE_TOOLS
from bots.tools.bot_phases.bot_phase import run_phase


def bot_compose(input):
  return run_phase(input, 'compose', COMPOSE_TOOLS)


BotCompose = Tool(
  name="BotCompose",
  description="Bot compose phase",
  func=bot_compose
)