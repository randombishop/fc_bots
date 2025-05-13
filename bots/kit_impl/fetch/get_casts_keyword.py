from bots.data.neynar import search_casts
from bots.kit_interface.casts import Casts
from bots.kit_interface.cast import Cast
from bots.kit_interface.keyword import Keyword


def get_casts_keyword(keyword: Keyword) -> Casts:
  keyword = keyword.keyword
  casts = search_casts(keyword, 'literal', 50)
  description = f'Casts with keyword "{keyword}"'
  if casts is None or len(casts) == 0:
    return Casts(description, [])
  casts.sort(key=lambda x: x['timestamp'])
  casts = [Cast(c) for c in casts]
  return Casts(description, casts)
