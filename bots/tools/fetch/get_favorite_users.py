from langchain.agents import Tool
from bots.data.users import get_favorite_users


def fetch(input):
  state = input.state
  fid = state.get('user_fid')
  df = get_favorite_users(fid)
  favorite_users = df.to_string(index=False)
  return {
    'favorite_users': favorite_users,
    'data_favorite_users': df
  }


GetFavoriteUsers = Tool(
  name="GetFavoriteUsers",
  description="Get the favorite accounts of a user.",
  metadata={
    'inputs': ['user_fid'],
    'outputs': ['favorite_users', 'data_favorite_users']
  },
  func=fetch
)
