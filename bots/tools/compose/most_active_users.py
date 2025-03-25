from langchain.agents import Tool
from bots.data.channels import get_channel_by_url


def compose_most_active_users(input):
  state = input.state
  channel_url = state.channel_url
  channel_id = get_channel_by_url(channel_url)
  chart = state.most_active_users_chart
  df = state.df_most_active_users
  if df is None or len(df) == 0 or chart is None:
    raise Exception("Missing most active users data")
  num_mentions = min(len(df), 3)
  mentions = [int(df.iloc[i]['fid']) for i in range(num_mentions)]
  mentions_ats = ['@'+df.iloc[i]['User'] for i in range(num_mentions)]
  mentions_positions = []
  users_label = "casters"
  if channel_id == 'mfers':
    users_label = "mfers"
  text = f"The most active {users_label}"
  if channel_id != 'mfers':
    text += f" in /{channel_id}"
  text += " are:\n"
  text += "🥇 "
  mentions_positions.append(len(text.encode('utf-8')))
  text += f" : {df.iloc[0]['casts_total']} casts.\n"
  if num_mentions > 1:
    text += "🥈 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += f" : {df.iloc[1]['casts_total']} casts.\n"
  if num_mentions > 2:
    text += "🥉 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += f" : {df.iloc[2]['casts_total']} casts.\n"
  cast = {
    'text': text, 
    'mentions': mentions, 
    'mentions_pos': mentions_positions,
    'mentions_ats': mentions_ats,
    'embeds': [chart],
    'embeds_description': "Chart of top active users in the channel"
  }
  casts =  [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposeMostActiveUsers = Tool(
  name="ComposeMostActiveUsers",
  description="Cast the most active users in a channel",
  func=compose_most_active_users
)
