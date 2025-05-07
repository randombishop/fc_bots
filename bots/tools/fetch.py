from langchain.agents import Tool
from bots.utils.functions import exec_function


def _fetch(input):
  return exec_function('retriever', input)


fetch = Tool(
  name="fetch",
  description="Execute a fetch method",
  func=_fetch
)