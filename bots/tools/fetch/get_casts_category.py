from langchain.agents import Tool
from bots.data.casts import get_top_casts
from bots.utils.format_cast import concat_casts


def fetch(input):
  state = input.state
  category = state.get('category')
  max_rows = state.get('max_rows')
  df = get_top_casts(category=category, max_rows=max_rows)
  posts = df.to_dict('records')
  posts.sort(key=lambda x: x['timestamp'])
  casts_category = f'Posts in category "{category}":\n' + concat_casts(posts)
  state.add_posts(posts)
  return {
    'casts_category': casts_category,
    'data_casts_category': posts
  }


GetCastsCategory = Tool(
  name="GetCastsCategory",
  description="Get posts using category parameter.",
  metadata={
    'inputs': ['category', 'max_rows'],
    'outputs': ['casts_category', 'data_casts_category']
  },
  func=fetch
)
