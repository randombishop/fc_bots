import random
from bots.i_wakeup_step import IWakeUpStep
from bots.data.bot_history import get_bot_channels
import pandas

class WakeUpChannelList(IWakeUpStep):
    
  def get(self, bot_character, bot_state):
    channels = get_bot_channels(bot_state.id)
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
    return channels
  