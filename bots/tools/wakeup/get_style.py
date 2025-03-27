import random
from langchain.agents import Tool


def get_style(input):
  state = input.state
  character = state.character
  style = None
  if character is not None and character['style'] is not None and len(character['style']) > 0:
    style = character['style']
    random.shuffle(style)
    state.style = '\n'.join(style)      
  return {'style': style}

GetStyle = Tool(
  name="GetStyle",
  func=get_style,
  description="Get the style of the bot."
)