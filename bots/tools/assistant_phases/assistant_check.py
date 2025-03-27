from langchain.agents import Tool
from bots.tools.check.shorten import Shorten
from bots.tools.check.validate import Validate


def check(input):
  shorten = Shorten.invoke({'input': input})
  valid = Validate.invoke({'input': input})
  return {'shorten': shorten, 'valid': valid}
    

AssistantCheck = Tool(
  name="AssistantCheck",
  description="Assistant check phase",
  metadata={
    'inputs': ['casts'],
    'outputs': ['check']
  },
  func=check
)