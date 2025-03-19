from langchain.agents import Tool
from bots.data.bot_history import get_bot_casts
from bots.utils.format_cast import shorten_text, format_when


def get_bot_casts(state):
  casts = get_bot_casts(state.id)
  text = ''
  for c in casts:
    row = '{\n'
    row += f"  prompt: {c['action_prompt']}\n"
    row += f"  post: {shorten_text(c['casted_text'])}\n"
    row += f"  channel: {c['action_channel']}\n"
    row += f"  when: {format_when(c['casted_at'])}\n"
    row += '}\n'
    text += row
  state.bot_casts = text


GetBotCasts = Tool(
  name="get_bot_casts",
  func=get_bot_casts,
  description="Get the bot's recent casts"
)