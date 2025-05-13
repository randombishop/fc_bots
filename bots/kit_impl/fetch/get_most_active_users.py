from bots.data.users import get_top_daily_casters
from bots.kit_interface.most_active_users import MostActiveUsers
from bots.kit_interface.channel_id import ChannelId


def get_most_active_users(channel_id: ChannelId) -> MostActiveUsers:
  df = get_top_daily_casters(channel_id.channel_url)
  return MostActiveUsers(channel_id, df)
