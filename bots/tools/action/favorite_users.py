import uuid
import os
from langchain.agents import Tool
from bots.data.users import get_favorite_users
from bots.utils.images import table_image
from bots.utils.gcs import upload_to_gcs


def favorite_users(input):
  state = input.state
  if state.action_params is None:
    raise Exception(f"Missing action_params")
  fid = state.action_params['fid']
  user_name = state.action_params['user_name']
  if fid is None or user_name is None:
    raise Exception(f"Missing fid or user_name")
  df = get_favorite_users(fid)
  if len(df) < 3:
    raise Exception(f"Not enough data ({len(df)})")
  df.rename(inplace=True, columns={
      'username': 'User',
      'num_recasts': 'Recasts',
      'num_likes': 'Likes',
      'num_replies': 'Replies'
  })
  filename = str(uuid.uuid4())+'.png'
  table_image(df[['User', 'Recasts', 'Likes', 'Replies']], filename)
  upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
  os.remove(filename)
  mentions = [int(df.iloc[i]['target_fid']) for i in range(3)]
  mentions_ats = ['@'+df.iloc[i]['User'] for i in range(3)]
  mentions_positions = []
  text = user_name+"'s favorite users are:\n"
  text += "🥇 "
  mentions_positions.append(len(text.encode('utf-8')))
  text += "\n"
  text += "🥈 "
  mentions_positions.append(len(text.encode('utf-8')))
  text += "\n"
  text += "🥉 "
  mentions_positions.append(len(text.encode('utf-8')))
  text += "\n"
  cast = {
    'text': text, 
    'mentions': mentions, 
    'mentions_pos': mentions_positions,
    'mentions_ats': mentions_ats,
    'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"],
    'embeds_description': 'Favorite users'
  }
  casts =  [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


FavoriteUsers = Tool(
  name="FavoriteUsers",
  description="Find the favorite accounts of a user",
  func=favorite_users,
  metadata={'depends_on': ['parse_favorite_users_params']}
)
