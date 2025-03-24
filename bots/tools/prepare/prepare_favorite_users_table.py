import uuid
import os
from langchain.agents import Tool
from bots.utils.images import table_image
from bots.utils.gcs import upload_to_gcs


def prepare_favorite_users_table(input):
  state = input.state
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
  state.favorite_users_table = f"https://fc.datascience.art/bot/main_files/{filename}"
  return {
    'favorite_users_table': state.favorite_users_table
  }


PrepareFavoriteUsersTable = Tool(
  name="PrepareFavoriteUsersTable",
  description="Prepare the favorite users table",
  func=prepare_favorite_users_table
)
