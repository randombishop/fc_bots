from langchain.agents import Tool
from bots.data.bot_history import get_bot_casts
from bots.utils.format_cast import format_bot_casts

def fetch(input):
  state = input.state
  id = state.get('id')
  name = state.get('name')
  channel = state.get('channel')
  casts = get_bot_casts(id, action_channel=channel)
  text = format_bot_casts(casts, name)
  return {
    'bot_casts_in_channel': text
  }


GetBotCastsInChannel = Tool(
  name="GetBotCastsInChannel",
  description="Get the casts posted by yourself (the bot) in a channel.",
  metadata={
    'inputs': ['id', 'channel'],
    'outputs': ['bot_casts_in_channel']
  },
  func=fetch
)

