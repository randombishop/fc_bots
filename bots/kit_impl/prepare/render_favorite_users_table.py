import uuid
import os
from bots.kit_interface.favorite_users import FavoriteUsers
from bots.kit_interface.favorite_users_table import FavoriteUsersTable
from bots.utils.images import table_image
from bots.utils.gcs import upload_to_gcs


def prepare(data: FavoriteUsers) -> FavoriteUsersTable:
  df = data.data
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
  url = f"https://fc.datascience.art/bot/main_files/{filename}"
  return FavoriteUsersTable(url)

