import pandas
from langchain.agents import Tool
from bots.data.bot_history import get_bot_channels


def get_channel_list(input):
  state = input.state
  channels = get_bot_channels(state.id)
  channels = [dict(c) for c in channels]
  for c in channels:
    if c['channel'] == '':
      c['channel'] = 'None'
      c['channel_activity'] = 9999
  channels = pandas.DataFrame(channels)
  channels['bot_activity'] = channels['bot_activity'].fillna(0).astype(int)
  channels['hours'] = channels['hours'].fillna(9999).astype(int)
  channels['channel_activity'] = channels['channel_activity'].fillna(0).astype(int)
  channels['avg_replies'] = channels['avg_replies'].fillna(0).astype(float)
  channels['avg_likes'] = channels['avg_likes'].fillna(0).astype(float)
  channels['avg_recasts'] = channels['avg_recasts'].fillna(0).astype(float)
  channels['avg_engagement'] = channels['avg_replies'] + channels['avg_likes']*2 + channels['avg_recasts']*3
  channels.sort_values(by='avg_engagement', ascending=False, inplace=True)
  channels.reset_index(drop=True, inplace=True)
  state.channel_list = channels
  return {'channel_list': channels}


GetChannelList = Tool(
  name="get_channel_list",
  func=get_channel_list,
  description="Get the list of channels for the bot"
)
  