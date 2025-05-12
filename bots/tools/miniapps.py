from langchain.agents import Tool
from bots.utils.functions import exec_function


def _miniapps(input):
  return exec_function('embedding', input)


miniapps = Tool(
  name="miniapps",
  description="Execute a miniapps method",
  func=_miniapps
)