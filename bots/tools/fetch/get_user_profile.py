from langchain.agents import Tool
from bots.data.wield import get_user_info_by_name
from bots.data.casts import get_top_casts
from bots.utils.format_cast import concat_casts


def fetch(input):
  state = input.state
  user_name = state.get('user')
  user_info = get_user_info_by_name(user_name)
  df = get_top_casts(user_name=user_name, max_rows=50)
  posts = df.to_dict('records') if len(df) > 0 else []
  casts_user = concat_casts(posts)
  data_casts_user = posts
  state.add_posts(data_casts_user)
  user_pfp_url = None
  if 'pfp' in user_info and user_info['pfp'] is not None and 'url' in user_info['pfp']:
    user_pfp_url = user_info['pfp']['url']
  return {
    'casts_user': casts_user,
    'data_casts_user': data_casts_user,
    'user_display_name': user_info['display_name'],
    'user_bio': user_info['bio']['text'] ,
    'user_followers': user_info['num_followers'],
    'user_following': user_info['num_following'],
    'user_pfp_url': user_pfp_url
  }
  

GetUserProfile = Tool(
  name="GetUserProfile",
  description="Fetch user profile data",
  metadata={
    'inputs': ['user'],
    'outputs': ['casts_user', 'data_casts_user', 'user_display_name', 'user_bio', 'user_followers', 'user_following', 'user_pfp_url']
  },
  func=fetch
)
