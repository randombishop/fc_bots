from langchain.agents import Tool
from bots.utils.functions import exec_function_runnable


def _memorize(input):
  return exec_function_runnable('embedding', input)


memorize = Tool(
  name="memorize",
  description="Memorizes elements of the current state",
  func=_memorize
)