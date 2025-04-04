from langchain.agents import Tool
from bots.utils.format_character import format_bio


def get_bio(input):    
  state = input.state
  character = state.character
  bio = format_bio(character)
  return {'bio': bio}
  
GetBio = Tool(
  name="GetBio",
  func=get_bio,
  description="Get the bio of the bot."
)