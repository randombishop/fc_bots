from langchain.agents import Tool
from bots.data.casts import get_top_casts
from bots.utils.format_cast import concat_casts


def fetch(input):
  state = input.state
  keyword = state.get('keyword')
  max_rows = state.get('max_rows')
  df = get_top_casts(keyword=keyword, max_rows=max_rows)
  posts = df.to_dict('records')
  posts.sort(key=lambda x: x['timestamp'])
  casts_keyword = f'Posts with keyword "{keyword}":\n' + concat_casts(posts)
  state.add_posts(posts)
  return {
    'casts_keyword': casts_keyword,
    'data_casts_keyword': posts
  }


desc = """Get posts using keyword parameter.
Use GetCastsKeyword when the instructions require searching for posts with a single keyword.
If the instructions indicate one particular keyword, use this tool (GetCastsKeyword), 
but if you need to search for a phrase with multiple words, use the other tool GetCastsSearchPhrase instead."""

GetCastsKeyword = Tool(
  name="GetCastsKeyword",
  description=desc,
  metadata={
    'inputs': ['keyword', 'max_rows'],
    'outputs': ['casts_keyword', 'data_casts_keyword']
  },
  func=fetch
)
