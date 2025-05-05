from langchain.agents import Tool
from bots.utils.functions import exec_function_runnable


def _fetch(input):
  return exec_function_runnable('retriever', input)


fetch = Tool(
  name="fetch",
  description="Execute a fetch method",
  func=_fetch
)