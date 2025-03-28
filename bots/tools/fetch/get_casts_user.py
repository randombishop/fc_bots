from langchain.agents import Tool
from bots.data.casts import get_top_casts
from bots.utils.format_cast import concat_casts


def fetch(input):
  state = input.state
  user_name = state.get('user')
  max_rows = state.get('max_rows')
  df = get_top_casts(user_name=user_name, max_rows=max_rows)
  posts = df.to_dict('records')
  posts.sort(key=lambda x: x['timestamp'])
  casts_user = f'Posts by @{user_name}:\n' + concat_casts(posts)
  data_casts_user = posts
  state.add_posts(data_casts_user)
  return {
    'casts_user': casts_user,
    'data_casts_user': data_casts_user
  }


GetCastsUser = Tool(
  name="GetCastsUser",
  description="Get posts by a user.",
  metadata={
    'inputs': ['user', 'user_fid'],
    'outputs': ['casts_user', 'data_casts_user']
  },
  func=fetch
)
