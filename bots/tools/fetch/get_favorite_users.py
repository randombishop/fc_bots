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
    'df_favorite_users': len(state.df_favorite_users) if state.df_favorite_users is not None else 0
  }


GetFavoriteUsers = Tool(
  name="GetFavoriteUsers",
  description="Fetch the favorite accounts of a user",
  func=get_favorite_users
)
