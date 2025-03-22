from langchain.agents import Tool
from bots.data.casts import get_top_casts, get_more_like_this


def get_casts_for_summary(input):
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
  state.casts_for_summary = posts
  return {
    'casts_for_summary': len(state.casts_for_summary)
  }


GetCastsForSummary = Tool(
  name="GetCastsForSummary",
  description="Fetch the casts to be summarized",
  func=get_casts_for_summary
)
