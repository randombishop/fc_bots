from bots.data.neynar import get_casts_channel as get_casts_data
from bots.kit_interface.cast import Cast
from bots.kit_interface.casts import Casts
from bots.kit_interface.channel_id import ChannelId


def get_casts_channel(channel_id: ChannelId) -> Casts:
  channel_url = channel_id.channel_url
  casts = get_casts_data(channel_url, 50)
  if casts is None or len(casts) == 0:
    return None
  casts.sort(key=lambda x: x['timestamp'])
  casts = [Cast(c) for c in casts]
  description = f'Casts in channel {channel_id.channel}'
  return Casts(description, casts)
