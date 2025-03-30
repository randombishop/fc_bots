from langchain.agents import Tool
from bots.tools.check.shorten import Shorten
from bots.tools.check.validate import Validate
from bots.tools.check.like import Like


def bot_check(input):
  state = input.state
  ans = {'checked': True}
  shorten = Shorten.invoke({'input': input})
  ans.update(shorten)
  valid = Validate.invoke({'input': input})
  ans.update(valid)
  if state.get('request') is not None:
    like = Like.invoke({'input': input})
    ans.update(like)
  return ans


CheckBot = Tool(
  name="CheckBot",
  description="Bot check phase",
  func=bot_check
)