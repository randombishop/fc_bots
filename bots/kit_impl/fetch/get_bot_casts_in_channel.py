from bots.data.neynar import get_casts_user_channel
from bots.kit_interface.channel_id import ChannelId
from bots.kit_interface.cast import Cast
from bots.kit_interface.casts import Casts


def get_bot_casts_in_channel(bot_id:int, channel_id:ChannelId) -> Casts:
  casts = get_casts_user_channel(bot_id, channel_id.channel_url, 50)
  if casts is None or len(casts) == 0:
    return None
  casts.sort(key=lambda x: x['timestamp'])
  casts = [Cast(c) for c in casts]
  description = f'Casts posted by the bot (yourself) in channel {channel_id.channel}'
  return Casts(description, casts)

