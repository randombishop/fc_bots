from bots.data.casts import get_trending_casts
from bots.kit_interface.cast import Cast
from bots.kit_interface.casts import Casts


def get_trending() -> Casts:
  casts = get_trending_casts(50)
  if casts is None or len(casts) == 0:
    return None
  casts.sort(key=lambda x: x['timestamp'])
  casts = [Cast(c) for c in casts]
  description = f'Globally trending casts'
  return Casts(description, casts)

