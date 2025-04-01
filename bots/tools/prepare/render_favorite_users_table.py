import uuid
import os
from langchain.agents import Tool
from bots.utils.images import table_image
from bots.utils.gcs import upload_to_gcs


def prepare(input):
  state = input.state
  df = state.get('data_favorite_users')
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
  favorite_users_table = f"https://fc.datascience.art/bot/main_files/{filename}"
  return {
    'favorite_users_table': favorite_users_table
  }


RenderFavoriteUsersTable = Tool(
  name="RenderFavoriteUsersTable",
  description="Prepare the favorite users table as an image",
  metadata={
    'inputs': ['data_favorite_users'],
    'outputs': ['favorite_users_table']
  },
  func=prepare
)
