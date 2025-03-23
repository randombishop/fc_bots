from langchain.agents import Tool
from bots.data.bot_history import get_bot_casts
from bots.utils.format_cast import shorten_text, format_when


def get_bot_casts_in_channel(input):
  state = input.state
  if state.channel is None:
    raise Exception('GetBotCastsInChannel requires a channel')
  casts = get_bot_casts(state.id, action_channel=state.channel)
  text = ''
  for c in casts:
    row = '{\n'
    row += f"  prompt: {c['action_prompt']}\n"
    row += f"  post: {shorten_text(c['casted_text'])}\n"
    row += f"  when: {format_when(c['casted_at'])}\n"
    row += '}\n'
    text += row
  state.bot_casts_in_channel = text


GetBotCastsInChannel = Tool(
  name="GetBotCastsInChannel",
  description="Get the casts of the bot in a channel",
  func=get_bot_casts_in_channel
)

