from langchain.agents import Tool
from bots.data.bot_history import get_bot_casts
from bots.utils.format_cast import shorten_text, format_when


def get_bot_casts_no_channel(input):
  state = input.state
  casts = get_bot_casts(state.id, no_channel=True)
  text = ''
  for c in casts:
    row = '{\n'
    row += f"  prompt: {c['action_prompt']}\n"
    row += f"  post: {shorten_text(c['casted_text'])}\n"
    row += f"  when: {format_when(c['casted_at'])}\n"
    row += '}\n'
    text += row
  state.bot_casts_no_channel = text
  return {
    'bot_casts_no_channel': state.bot_casts_no_channel
  }


GetBotCastsNoChannel = Tool(
  name="GetBotCastsNoChannel",
  description="Get the casts of the bot in main feed.",
  metadata={
    'outputs': 'bot_casts_no_channel'
  },
  func=get_bot_casts_no_channel
)

