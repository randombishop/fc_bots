import random
from langchain.agents import Tool

SAMPLE_SIZE = 5

def get_lore(input):
  state = input.state
  if state.character is not None and state.character['lore'] is not None and len(state.character['lore']) > 0:
    lore = state.character['lore']
    if len(lore)>SAMPLE_SIZE:
      lore = random.sample(lore, SAMPLE_SIZE)
    random.shuffle(lore)
    state.lore = '\n'.join(lore)
  else:
    state.lore =''
  return {'lore': state.lore}
  
GetLore = Tool(
  name="get_lore",
  func=get_lore,
  description="Get the lore of the bot."
)
  
  