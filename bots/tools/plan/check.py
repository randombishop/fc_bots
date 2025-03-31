from langchain.agents import Tool
from bots.tools.check.shorten import Shorten
from bots.tools.check.validate import Validate
from bots.tools.check.like import Like


def check(input):
  state = input.state
  ans = {'checked': True}
  shorten = Shorten.invoke({'input': input})
  ans.update(shorten)
  valid = Validate.invoke({'input': input})
  ans.update(valid)
  if state.get('mode') == 'bot':
    like = Like.invoke({'input': input})
    ans.update(like)
  return ans
    

Check = Tool(
  name="Check",
  description="Check outputs phase",
  func=check
)