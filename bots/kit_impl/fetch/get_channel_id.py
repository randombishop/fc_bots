from bots.kit_interface.channel_id import ChannelId
from bots.utils.read_params import read_channel
from bots.data.channels import get_channel_by_url


def get_channel_id(parsed_channel: str) -> ChannelId:
  params = {'channel': parsed_channel}
  channel_url = read_channel(params)
  channel = get_channel_by_url(channel_url)
  if channel is not None and channel_url is not None:
    return ChannelId(channel, channel_url)
  else:
    return None
