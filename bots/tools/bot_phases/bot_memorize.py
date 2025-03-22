from langchain.agents import Tool
from bots.tools.memorize.save_user_profile import SaveUserProfile


def bot_memorize(input):
  state = input.state
  memorized = [] 
  if state.selected_action in ['Praise', 'WhoIs']:
    SaveUserProfile.invoke({'input': input})
    memorized.append('user_profile')
  return {
    'memorized': memorized
  }


BotMemorize = Tool(
  name="BotMemorize",
  description="Bot memorize phase",
  func=bot_memorize
)