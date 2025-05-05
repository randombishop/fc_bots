from bots.data.neynar import get_user_info_by_name
from bots.kit_interface.user_profile import UserProfile


def get_user_profile(username: str) -> UserProfile:
  user_info = get_user_info_by_name(username)
  if user_info is None:
    return None
  return UserProfile(
    display_name=user_info['display_name'],
    bio=user_info['bio'],
    followers=user_info['num_followers'],
    following=user_info['num_following'],
    pfp_url=user_info['pfp']
  )
  
