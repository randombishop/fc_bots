from bots.tools.fetch.aggregate_casts import AggregateCasts
from bots.tools.fetch.get_bot_casts_in_channel import GetBotCastsInChannel
from bots.tools.fetch.get_bot_casts import GetBotCasts
from bots.tools.fetch.get_casts_category import GetCastsCategory
from bots.tools.fetch.get_casts_channel import GetCastsChannel
from bots.tools.fetch.get_casts_keyword import GetCastsKeyword
from bots.tools.fetch.get_casts_search import GetCastsSearch
from bots.tools.fetch.get_casts_user import GetCastsUser
from bots.tools.fetch.get_favorite_users import GetFavoriteUsers
from bots.tools.fetch.get_more_like_this import GetMoreLikeThis
from bots.tools.fetch.get_most_active_users import GetMostActiveUsers
from bots.tools.fetch.get_news import GetNews
from bots.tools.fetch.get_trending import GetTrending
from bots.tools.fetch.get_user_profile import GetUserProfile
from bots.tools.fetch.get_user_stats import GetUserStats
from bots.tools.fetch.get_user_replies_and_reactions import GetUserRepliesAndReactions



FETCH_TOOLS = [
  AggregateCasts,
  GetBotCastsInChannel,
  GetBotCasts,
  GetCastsCategory,
  GetCastsChannel,
  GetCastsKeyword,  
  GetCastsSearch,
  GetCastsUser,
  GetFavoriteUsers,
  GetMoreLikeThis,
  GetMostActiveUsers,
  GetNews,
  GetTrending,
  GetUserProfile,
  GetUserStats,
  GetUserRepliesAndReactions  
]