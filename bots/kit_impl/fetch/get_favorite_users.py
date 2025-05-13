from bots.data.users import get_favorite_users as get_data_frame
from bots.kit_interface.favorite_users import FavoriteUsers


def get_favorite_users(fid: int) -> FavoriteUsers:
  df = get_data_frame(fid)
  return FavoriteUsers(df)
