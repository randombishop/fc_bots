from bots.i_prepare_step import IPrepareStep
from bots.data.channels import get_channel_url
from bots.data.casts import get_top_casts
from bots.prompts.format_casts import concat_casts



class GetChannelCasts(IPrepareStep):
    
  def prepare(self):
    if self.state.channel is None:
      raise Exception('GetChannelCasts requires a channel')
    channel_url = get_channel_url(self.state.channel)
    if channel_url is None:
      raise Exception('GetChannelCasts could not map channel to url')
    max_rows = 25
    posts = get_top_casts(channel=channel_url, max_rows=max_rows)
    if posts is not None and len(posts)>0:
      posts = posts.to_dict('records')
      self.state.sample_casts_in_channel = concat_casts(posts)
      for p in posts:
        self.state.posts_map[p['id']] = p
    else:
      self.state.sample_casts_in_channel = ''
