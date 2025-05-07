from langchain.agents import Tool
from bots.utils.functions import exec_function


def _memorize(input):
  return exec_function('embedding', input)


memorize = Tool(
  name="memorize",
  description="Memorizes elements of the current state",
  func=_memorize
)