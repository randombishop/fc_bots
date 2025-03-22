from langchain.agents import Tool
from bots.data.casts import get_top_casts, get_more_like_this


def get_casts_for_params(input):
  state = input.state
  posts = []
  if state.search is not None:
    posts = get_more_like_this(state.search, limit=state.max_rows)
  else:
    posts = get_top_casts(channel=state.channel_url,
                          keyword=state.keyword,
                          category=state.category,
                          user_name=state.user,
                          max_rows=state.max_rows)
  posts = posts.to_dict('records')
  posts.sort(key=lambda x: x['timestamp'])
  state.casts_for_params = posts
  return {
    'casts_for_params': len(state.casts_for_params)
  }


GetCastsForParams = Tool(
  name="GetCastsForParams",
  description="Fetch casts based on current parameters",
  func=get_casts_for_params
)
