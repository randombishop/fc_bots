from langchain.agents import Tool
from bots.utils.format_character import format_lore


def get_lore(input):
  state = input.state
  character = state.character
  lore = format_lore(character)
  return {'lore': lore}
  
GetLore = Tool(
  name="GetLore",
  func=get_lore,
  description="Get the lore of the bot."
)
  
  