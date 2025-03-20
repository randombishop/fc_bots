from bots.v2.tools.fetch.get_bot_casts_in_channel import GetBotCastsInChannel
from bots.v2.tools.fetch.get_bot_casts_no_channel import GetBotCastsNoChannel
from bots.v2.tools.fetch.get_bot_casts import GetBotCasts
from bots.v2.tools.fetch.get_casts import GetCasts
from bots.v2.tools.fetch.get_channel_list import GetChannelList
from bots.v2.tools.fetch.get_trending import GetTrending


FETCH_TOOLS = [
  GetBotCastsInChannel,
  GetBotCastsNoChannel,
  GetBotCasts,
  GetCasts,
  GetChannelList,
  GetTrending
]