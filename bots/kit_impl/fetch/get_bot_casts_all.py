from bots.data.neynar import get_casts_user
from bots.kit_interface.casts import Casts
from bots.kit_interface.cast import Cast


def get_bot_casts_all(bot_id: int) -> Casts:
  casts = get_casts_user(bot_id, 50)
  if casts is None or len(casts) == 0:
    return None
  casts.sort(key=lambda x: x['timestamp'])
  casts = [Cast(c) for c in casts]
  description = f'All casts from the bot (yourself)'
  return Casts(description, casts)