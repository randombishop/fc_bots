import random
from langchain.agents import Tool
from bots.action.action_steps import DESCRIPTIONS

RANDOMIZE = True

def get_actions(input):    
  state = input['state']
  character = state.character
  if character['action_steps'] is not None and len(character['action_steps']) > 0:
    actions = character['action_steps']
    if RANDOMIZE:
      random.shuffle(actions)
    ans = ''
    for action in actions:
      ans += f'{action}: {DESCRIPTIONS[action]}\n'
    state.actions = ans
  return {'actions': state.actions}


GetActions = Tool(
  name="get_actions",
  func=get_actions,
  description="Get the available actions for the bot"
)
  
  