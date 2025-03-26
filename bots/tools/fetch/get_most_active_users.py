from langchain.agents import Tool
from bots.data.users import get_top_daily_casters


def get_most_active_users(input):
  state = input.state
  channel_url = state.channel_url
  if channel_url is None:
    raise Exception("Missing channel")
  df = get_top_daily_casters(channel_url)
  state.df_most_active_users = df
  return {
    'df_most_active_users': state.df_most_active_users
  }


GetMostActiveUsers = Tool(
  name="GetMostActiveUsers",
  description="Find the most active users in a channel",
  metadata={
    'inputs': 'Requires channel parameter. Will fail if not set.',
    'outputs': 'Dataframe df_most_active_users'
  },
  func=get_most_active_users
)
