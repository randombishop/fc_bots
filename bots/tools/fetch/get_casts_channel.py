from langchain.agents import Tool
from bots.data.casts import get_top_casts
from bots.utils.format_cast import concat_casts


def fetch(input):
  state = input.state
  channel = state.get('channel')
  channel_url = state.get('channel_url')
  max_rows = state.get('max_rows')
  df = get_top_casts(channel=channel_url, max_rows=max_rows)
  posts = df.to_dict('records')
  posts.sort(key=lambda x: x['timestamp'])
  casts_channel = f'Posts in channel {channel}:\n' + concat_casts(posts)
  state.add_posts(posts)
  return {
    'casts_channel': casts_channel,
    'data_casts_channel': posts
  }


GetCastsChannel = Tool(
  name="GetCastsChannel",
  description="Get posts in a channel.",
  metadata={
    'inputs': ['channel_url', 'max_rows'],
    'outputs': ['casts_channel', 'data_casts_channel']
  },
  func=fetch
)
