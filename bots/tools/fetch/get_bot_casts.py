from langchain.agents import Tool
from bots.data import bot_history
from bots.utils.format_cast import format_bot_casts


def fetch(input):
  state = input.state
  id = state.get('id')
  name = state.get('name')
  casts = bot_history.get_bot_casts(id)
  text = format_bot_casts(casts, name)
  return {'bot_casts': text}


GetBotCasts = Tool(
  name="GetBotCasts",
  description="Get all recent casts posted by yourself (the bot).",
  metadata={
    'inputs': ['id'],
    'outputs': ['bot_casts']
  },
  func=fetch
)