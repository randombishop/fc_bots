from langchain.agents import Tool
from bots.data import bot_history
from bots.utils.format_cast import shorten_text, format_when


def fetch(input):
  state = input.state
  id = state.get('id')
  casts = bot_history.get_bot_casts(id)
  text = ''
  for c in casts:
    row = '{\n'
    row += f"  prompt: {c['action_prompt']}\n"
    row += f"  post: {shorten_text(c['casted_text'])}\n"
    row += f"  channel: {c['action_channel']}\n"
    row += f"  when: {format_when(c['casted_at'])}\n"
    row += '}\n'
    text += row
  return {'bot_casts': text}


GetBotCasts = Tool(
  name="GetBotCasts",
  description="Get the bot's recent casts.",
  metadata={
    'inputs': ['id'],
    'outputs': ['bot_casts']
  },
  func=fetch
)