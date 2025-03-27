import random
from langchain.agents import Tool

SAMPLE_SIZE = 5

def get_lore(input):
  state = input.state
  character = state.get('character')
  lore = None
  if character is not None and character['lore'] is not None and len(character['lore']) > 0:
    lore = character['lore']
    if len(lore)>SAMPLE_SIZE:
      lore = random.sample(lore, SAMPLE_SIZE)
    random.shuffle(lore)
    lore = '\n'.join(lore)
  return {'lore': lore}
  

GetLore = Tool(
  name="GetLore",
  func=get_lore,
  description="Get the lore of the bot."
)
  
  