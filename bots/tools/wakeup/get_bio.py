import random
from langchain.agents import Tool

SAMPLE_SIZE = 5

def get_bio(input):    
  state = input['state']
  if state.character is not None and state.character['bio'] is not None and len(state.character['bio']) > 0:
    bio = state.character['bio']
    if len(bio)>SAMPLE_SIZE:
      bio = random.sample(bio, SAMPLE_SIZE)
    random.shuffle(bio)
    state.bio = '\n'.join(bio)      
  else:
    state.bio = ''
  return {'bio': state.bio}
  
GetBio = Tool(
  name="get_bio",
  func=get_bio,
  description="Get the bio of the bot."
)