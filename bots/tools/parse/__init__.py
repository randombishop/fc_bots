from bots.tools.parse.make_user_stats_sql_query import MakeUserStatsSQLQuery
from bots.tools.parse.parse_category import ParseCategory
from bots.tools.parse.parse_channel import ParseChannel
from bots.tools.parse.parse_keyword import ParseKeyword
from bots.tools.parse.parse_more_like_this_text import ParseMoreLikeThisText
from bots.tools.parse.parse_news_search import ParseNewsSearch
from bots.tools.parse.parse_perplexity_question import ParsePerplexityQuestion
from bots.tools.parse.parse_search_phrase import ParseSearchPhrase
from bots.tools.parse.parse_user import ParseUser
from bots.tools.parse.select_random_user import SelectRandomUser


PARSE_TOOLS = [
  MakeUserStatsSQLQuery,
  ParseCategory,
  ParseChannel,
  ParseKeyword,
  ParseMoreLikeThisText,
  ParseNewsSearch,
  ParsePerplexityQuestion,
  ParseSearchPhrase,
  ParseUser,
  SelectRandomUser
]