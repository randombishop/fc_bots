from langchain.agents import Tool
from bots.data.channels import get_channel_url
from bots.data.casts import get_top_casts
from bots.prompts.format_casts import concat_casts



def get_casts_in_channel(input):
  state = input['state']
  if state.selected_channel is None:
    raise Exception('GetChannelCasts requires a channel')
  channel_url = get_channel_url(state.selected_channel)
  if channel_url is None:
    raise Exception('GetChannelCasts could not map channel to url')
  max_rows = 25
  posts = get_top_casts(channel=channel_url, max_rows=max_rows)
  if posts is not None and len(posts)>0:
    posts = posts.to_dict('records')
    state.casts_in_channel = concat_casts(posts)
    for p in posts:
      state.posts_map[p['id']] = p
  else:
    state.casts_in_channel = ''
  return {
    'casts_in_channel': state.casts_in_channel
  }


GetCastsInChannel = Tool(
  name="GetCastsInChannel",
  description="Get the casts in a channel",
  func=get_casts_in_channel
)
  