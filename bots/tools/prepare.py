from langchain.agents import Tool
from bots.utils.functions import exec_function_runnable


def _prepare(input):
  return exec_function_runnable('chain', input)


prepare = Tool(
  name="prepare",
  description="Execute a prepare method",
  func=_prepare
)