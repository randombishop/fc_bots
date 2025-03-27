from langchain.agents import Tool
from bots.data.casts import get_more_like_this
from bots.utils.format_cast import concat_casts


def fetch(input):
  state = input.state
  search = state.get('search')
  max_rows = state.get('max_rows')
  df = get_more_like_this(search, limit=max_rows)
  posts = df.to_dict('records')
  posts.sort(key=lambda x: x['timestamp'])
  casts_search = f'Posts search result for "{search}":\n' + concat_casts(posts)
  state.add_posts(posts)
  return {
    'casts_search': casts_search,
    'data_casts_search': posts
  }


GetCastsSearch = Tool(
  name="GetCastsSearch",
  description="Search for posts using search parameter.",
  metadata={
    'inputs': ['search', 'max_rows'],
    'outputs': ['casts_search', 'data_casts_search']
  },
  func=fetch
)
