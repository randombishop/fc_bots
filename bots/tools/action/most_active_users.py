import uuid
import os
from langchain.agents import Tool
from bots.data.users import get_top_daily_casters
from bots.utils.images import user_activity_chart
from bots.utils.gcs import upload_to_gcs
from bots.data.channels import get_channel_by_url


def most_active_users(input):
  state = input['state']
  channel_url = state.action_params['channel']
  if channel_url is None:
    raise Exception("Missing channel")
  channel_id = get_channel_by_url(channel_url)
  if channel_id is None:
    raise Exception("Channel not registered")
  df = get_top_daily_casters(channel_url)
  if len(df) == 0:
    raise Exception("Query returned 0 rows")
  filename = str(uuid.uuid4())+'.png'
  user_activity_chart(df, filename)
  upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
  os.remove(filename)
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
    'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"],
    'embeds_description': "Chart of top active users in the channel"
  }
  casts =  [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


MostActiveUsers = Tool(
  name="MostActiveUsers",
  description="Find the most active users in a channel",
  func=most_active_users,
  metadata={'depends_on': ['parse_most_active_users_params']}
)
