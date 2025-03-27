import random
from langchain.agents import Tool

SAMPLE_SIZE = 5

def get_bio(input):    
  state = input.state
  character = state.get('character')
  bio = None
  if character is not None and character['bio'] is not None and len(character['bio']) > 0:
    bio = character['bio']
    if len(bio)>SAMPLE_SIZE:
      bio = random.sample(bio, SAMPLE_SIZE)
    random.shuffle(bio)
    bio = '\n'.join(bio)      
  return {'bio': bio}
  
GetBio = Tool(
  name="GetBio",
  func=get_bio,
  description="Get the bio of the bot."
)