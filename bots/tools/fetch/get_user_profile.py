from langchain.agents import Tool
from bots.data.wield import get_user_info_by_name


def fetch(input):
  state = input.state
  user_name = state.get('user')
  user_info = get_user_info_by_name(user_name)
  user_pfp_url = None
  if 'pfp' in user_info and user_info['pfp'] is not None and 'url' in user_info['pfp']:
    user_pfp_url = user_info['pfp']['url']
  return {
    'user_display_name': user_info['display_name'],
    'user_bio': user_info['bio']['text'] ,
    'user_followers': user_info['num_followers'],
    'user_following': user_info['num_following'],
    'user_pfp_url': user_pfp_url
  }
  

GetUserProfile = Tool(
  name="GetUserProfile",
  description="Fetch user profile data",
  metadata={
    'inputs': ['user'],
    'outputs': ['user_display_name', 'user_bio', 'user_followers', 'user_following', 'user_pfp_url']
  },
  func=fetch
)
