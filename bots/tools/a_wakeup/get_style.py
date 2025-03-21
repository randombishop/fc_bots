import random
from langchain.agents import Tool


def get_style(input):
  state = input.state
  if state.character is not None and state.character['style'] is not None and len(state.character['style']) > 0:
    style = state.character['style']
    random.shuffle(style)
    state.style = '\n'.join(style)      
  else:
    state.style = ''
  return {'style': state.style}

GetStyle = Tool(
  name="get_style",
  func=get_style,
  description="Get the style of the bot."
)
  
  