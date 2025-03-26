import random
from langchain.agents import Tool


ACTION_DESCRIPTIONS = {
  'Chat': 'Default action if no other intent is applicable.',
  'Summary': 'Make a summary about posts.',
  'FavoriteUsers': 'Find the favorite accounts of a user.',
  'MoreLikeThis': 'Find posts using "More Like This" algorithm.',
  'MostActiveUsers': 'List the most active users in a channel.',
  'News': 'Check the news.',
  'Perplexity': 'Ask a question to Perplexity AI.',
  'Pick': 'Pick a post given some criteria.',
  'Psycho': 'Generate a psychoanalysis for a user.',
  'Praise': 'Generate a praise for a user.',
  'Roast': 'Generate a roast for a user.',
  'WhoIs': 'Analyze a user profile and generate a new avatar for them. (Who is @user? Make an avater for @user, Analyze user profile @user, etc.)',
  'WordCloud': 'Make a word cloud.'
}


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
  
  