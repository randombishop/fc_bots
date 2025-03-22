import uuid
import os
from langchain.agents import Tool
from bots.utils.images import table_image
from bots.utils.gcs import upload_to_gcs


def compose_favorite_users(input):
  state = input.state
  fid = state.user_fid
  user_name = state.user
  if fid is None or user_name is None:
    raise Exception(f"Missing fid or user_name")
  df = state.df_favorite_users
  if df is None:
    raise Exception(f"Favorite users data not found")
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


ComposeFavoriteUsers = Tool(
  name="ComposeFavoriteUsers",
  description="Cast the favorite accounts of a user",
  func=compose_favorite_users
)
