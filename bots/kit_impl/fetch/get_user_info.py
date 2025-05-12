from bots.data.neynar import get_user_info_by_name
from bots.kit_interface.user_info import UserInfo


def get_user_info(username: str) -> UserInfo:
  user_info = get_user_info_by_name(username)
  if user_info is None:
    return None
  return UserInfo(
    display_name=user_info['display_name'],
    bio=user_info['bio'],
    followers=user_info['num_followers'],
    following=user_info['num_following'],
    pfp_url=user_info['pfp']
  )
  
