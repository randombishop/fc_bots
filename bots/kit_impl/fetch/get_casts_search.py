from bots.data.neynar import search_casts
from bots.kit_interface.casts import Casts
from bots.kit_interface.cast import Cast
from bots.kit_interface.search_phrase import SearchPhrase


def get_casts_search(search_phrase: SearchPhrase) -> Casts:
  search = search_phrase.search
  casts = search_casts(search, 'semantic', 50)
  description = f'Cast results for "{search}"'
  if casts is None or len(casts) == 0:
    return Casts(description, [])
  casts.sort(key=lambda x: x['timestamp'])
  casts = [Cast(c) for c in casts]
  return Casts(description, casts)
