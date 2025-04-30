from bots.kit_interface.user_id import UserId
from bots.utils.read_params import read_user


def get_user_id(user: str) -> UserId:
  params = {'user': user}
  fid, user_name = read_user(params)
  if fid is None or user_name is None:
    return None
  else:
    return UserId(fid, user_name)
  
