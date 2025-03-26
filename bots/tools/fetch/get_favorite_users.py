from langchain.agents import Tool
from bots.data.users import get_favorite_users as get_favorite_users_data


def get_favorite_users(input):
  state = input.state
  fid = state.user_fid
  user_name = state.user
  if fid is None or user_name is None:
    raise Exception(f"Missing fid or user_name")
  df = get_favorite_users_data(fid)
  state.df_favorite_users = df
  return {
    'df_favorite_users': state.df_favorite_users
  }


GetFavoriteUsers = Tool(
  name="GetFavoriteUsers",
  description="Get the favorite accounts of a user.",
  metadata={
    'inputs': 'Will fail if fid or user_name are not set',
    'outputs': 'Dataframe df_favorite_users'
  },
  func=get_favorite_users
)
