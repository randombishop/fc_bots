from langchain.agents import Tool
from bots.tools.check.shorten import Shorten
from bots.tools.check.validate import Validate


def check(input):
  ans = {'checked': True}
  shorten = Shorten.invoke({'input': input})
  ans.update(shorten)
  valid = Validate.invoke({'input': input})
  ans.update(valid)
  return ans
    

Check = Tool(
  name="Check",
  description="Check outputs phase",
  func=check
)