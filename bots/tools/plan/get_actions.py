import random
from langchain.agents import Tool
from bots.tools.actions import ACTION_DESCRIPTIONS


RANDOMIZE = True

def get_actions(input):    
  state = input.state
  character = state.character
  if character['action_steps'] is not None and len(character['action_steps']) > 0:
    actions = character['action_steps']
    if RANDOMIZE:
      random.shuffle(actions)
    ans = ''
    for action in actions:
      include = action != 'Chat' or state.is_responding()
      if include:
        ans += f'{action}: {ACTION_DESCRIPTIONS[action]}\n'
    state.actions = ans
  return {'actions': state.actions}

GetActions = Tool(
  name="GetActions",
  func=get_actions,
  description="Get the available actions for the bot"
)
  
  