from bots.i_prepare_step import IPrepareStep
from bots.data.wield import get_user_info_by_name
from bots.data.casts import get_top_casts
from bots.prompts.format_casts import concat_casts


class GetUserProfile(IPrepareStep):
    
  def prepare(self):
    user_name = self.state.user
    if user_name is None:
      raise Exception(f"Missing user name in context.")
    user_info = get_user_info_by_name(user_name)
    df = get_top_casts(user_name=user_name, max_rows=25)
    if df is None or len(df) == 0:
      raise Exception(f"Not enough activity to build a user profile.")
    posts = df.to_dict('records')
    formatted_posts = concat_casts(posts)
    self.state.user_casts = posts
    for x in posts:
      self.state.posts_map[x['id']] = x
    self.state.about_user = formatted_posts
    self.state.user_display_name = user_info['display_name'] +'\n\n'
    self.state.user_bio = user_info['bio']['text'] +'\n\n'
    if 'pfp' in user_info and user_info['pfp'] is not None and 'url' in user_info['pfp']:
      self.state.user_pfp_url = user_info['pfp']['url']
    log = '<GetUserProfile>\n'
    log += f"posts: {len(posts)}\n"
    log += f"display_name: {self.state.user_display_name}\n"
    log += f"bio: {self.state.user_bio}\n"
    log += f"pfp_url: {self.state.user_pfp_url}\n"
    log += '</GetUserProfile>\n'
    self.state.log += log
  