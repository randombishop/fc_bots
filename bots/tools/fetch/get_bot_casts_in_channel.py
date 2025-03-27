from langchain.agents import Tool
from bots.data.bot_history import get_bot_casts
from bots.utils.format_cast import shorten_text, format_when


def fetch(input):
  state = input.state
  id = state.get('id')
  channel = state.get('channel')
  casts = get_bot_casts(id, action_channel=channel)
  text = ''
  for c in casts:
    row = '{\n'
    row += f"  prompt: {c['action_prompt']}\n"
    row += f"  post: {shorten_text(c['casted_text'])}\n"
    row += f"  when: {format_when(c['casted_at'])}\n"
    row += '}\n'
    text += row
  return {
    'bot_casts_in_channel': text
  }


GetBotCastsInChannel = Tool(
  name="GetBotCastsInChannel",
  description="Get the casts of the bot in a channel.",
  metadata={
    'inputs': ['id', 'channel'],
    'outputs': ['bot_casts_in_channel']
  },
  func=fetch
)

