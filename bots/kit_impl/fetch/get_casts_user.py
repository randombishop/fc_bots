from bots.data.neynar import get_casts_user
from bots.kit_interface.casts import Casts
from bots.kit_interface.cast import Cast
from bots.kit_interface.user_id import UserId


def get_casts_user(user_id: UserId) -> Casts:
  fid = user_id.fid
  username = user_id.username
  casts = get_casts_user(fid, 50)
  if casts is None or len(casts) == 0:
    return None
  casts.sort(key=lambda x: x['timestamp'])
  casts = [Cast(c) for c in casts]
  description = f'Casts from @{username}'
  return Casts(description, casts)
