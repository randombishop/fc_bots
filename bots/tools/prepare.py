from langchain.agents import Tool
from bots.utils.functions import exec_function


def _prepare(input):
  return exec_function('chain', input)


prepare = Tool(
  name="prepare",
  description="Execute a prepare method",
  func=_prepare
)