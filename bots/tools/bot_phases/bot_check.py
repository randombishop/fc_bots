from langchain.agents import Tool
from bots.tools.check.shorten import Shorten
from bots.tools.check.validate import Validate
from bots.tools.check.like import Like


def bot_check(input):
  state = input.state
  if state.casts is not None and len(state.casts) > 0:
    Shorten.invoke({'input': input})
    Validate.invoke({'input': input})
  if state.is_responding():
    Like.invoke({'input': input})
  return {
    'reply': state.reply,
    'like': state.like
  }


BotCheck = Tool(
  name="BotCheck",
  description="Bot check phase",
  func=bot_check
)