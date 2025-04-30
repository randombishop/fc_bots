from bots.kit_interface.channel_id import ChannelId
from bots.kit_interface.user_id import UserId
from bots.data.bot_history import get_random_user, get_random_user_in_channel
from bots.data.users import get_fid


def get_random_user(bot_id: int, channel_id: ChannelId|None) -> UserId:
  user_name, fid = None, None
  if channel_id is None:
    user_name = get_random_user(bot_id)
    fid = get_fid(user_name)  
  else:
    channel_url = channel_id.channel_url
    user_name = get_random_user_in_channel(bot_id, channel_url)
    fid = get_fid(user_name)
  if fid is None or user_name is None:
    return None
  else:
    return UserId(fid, user_name)
 