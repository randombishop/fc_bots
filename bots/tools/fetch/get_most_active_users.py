from langchain.agents import Tool
from bots.data.users import get_top_daily_casters


def fetch(input):
  state = input.state
  channel_url = state.get('channel_url')
  df = get_top_daily_casters(channel_url)
  most_active_users = ''
  rows = df.to_dict('records') if len(df) > 0 else []
  for r in rows:
    text = f"@{r['User']} posted {r['casts_total']} times\n"
    most_active_users += text
  return {
    'data_most_active_users': df,
    'most_active_users': most_active_users
  }


GetMostActiveUsers = Tool(
  name="GetMostActiveUsers",
  description="Find the most active users in a channel",
  metadata={
    'inputs': ['channel_url'],
    'outputs': ['data_most_active_users', 'most_active_users']
  },
  func=fetch
)
