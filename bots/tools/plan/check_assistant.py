from langchain.agents import Tool
from bots.tools.check.shorten import Shorten
from bots.tools.check.validate import Validate


def check(input):
  ans = {}
  shorten = Shorten.invoke({'input': input})
  ans.update(shorten)
  valid = Validate.invoke({'input': input})
  ans.update(valid)
  state = input.state
  state.checked = True
  return ans
    

CheckAssistant = Tool(
  name="CheckAssistant",
  description="Assistant check phase",
  metadata={
    'inputs': ['casts'],
    'outputs': ['check']
  },
  func=check
)