from bots.utils.read_params import read_string
from bots.kit_interface.search_phrase import SearchPhrase


def get_search_phrase(search: str) -> SearchPhrase:
  params = {'search': search}
  search = read_string(params, key='search', max_length=500)
  return SearchPhrase(search)

