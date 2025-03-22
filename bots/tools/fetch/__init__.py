from bots.tools.fetch.get_bot_casts_in_channel import GetBotCastsInChannel
from bots.tools.fetch.get_bot_casts_no_channel import GetBotCastsNoChannel
from bots.tools.fetch.get_bot_casts import GetBotCasts
from bots.tools.fetch.get_casts_for_fid import GetCastsForFid
from bots.tools.fetch.get_casts_for_params import GetCastsForParams
from bots.tools.fetch.get_casts_for_context import GetCastsForContext
from bots.tools.fetch.get_channel_list import GetChannelList
from bots.tools.fetch.get_favorite_users import GetFavoriteUsers
from bots.tools.fetch.get_more_like_this import GetMoreLikeThis
from bots.tools.fetch.get_most_active_users import GetMostActiveUsers
from bots.tools.fetch.get_trending import GetTrending


FETCH_TOOLS = [
  GetBotCastsInChannel,
  GetBotCastsNoChannel,
  GetBotCasts,
  GetCastsForFid,
  GetCastsForParams,
  GetCastsForContext,
  GetChannelList, 
  GetFavoriteUsers,
  GetMoreLikeThis,
  GetMostActiveUsers,
  GetTrending
]