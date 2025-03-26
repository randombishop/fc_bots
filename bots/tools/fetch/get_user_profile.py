from langchain.agents import Tool
from bots.data.wield import get_user_info_by_name
from bots.data.casts import get_top_casts
from bots.utils.format_cast import concat_casts


def get_user_profile(input):
  state = input.state
  if state.user_casts_description is not None:
    return {'log': 'User profile already set.'}
  user_name = state.user
  if user_name is None:
    raise Exception(f"Missing user name in context.")
  user_info = get_user_info_by_name(user_name)
  df = get_top_casts(user_name=user_name, max_rows=50)
  posts = df.to_dict('records') if len(df) > 0 else []
  state.user_casts = concat_casts(posts)
  state.user_casts_data = posts
  for x in posts:
    state.posts_map[x['id']] = x
  state.user_display_name = user_info['display_name']
  state.user_bio = user_info['bio']['text'] 
  state.user_followers = user_info['num_followers']
  state.user_following = user_info['num_following']
  if 'pfp' in user_info and user_info['pfp'] is not None and 'url' in user_info['pfp']:
    state.user_pfp_url = user_info['pfp']['url']
  return {
    'user_casts': state.user_casts,
    'user_display_name': state.user_display_name,
    'user_bio': state.user_bio,
    'user_followers': state.user_followers,
    'user_following': state.user_following,
    'user_pfp_url': state.user_pfp_url,
  }
  

GetUserProfile = Tool(
  name="GetUserProfile",
  description="Fetch user profile data",
  metadata={
    'inputs': 'Requires user parameter',
    'outputs': 'user_casts, user_display_name, user_bio, user_followers, user_following, user_pfp_url'
  },
  func=get_user_profile
)
