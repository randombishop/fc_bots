from bots.tools.parse.parse_category import ParseCategory
from bots.tools.parse.parse_channel import ParseChannel
from bots.tools.parse.parse_keyword_and_search import ParseKeywordAndSearch
from bots.tools.parse.parse_more_like_this_text import ParseMoreLikeThisText
from bots.tools.parse.parse_news_search import ParseNewsSearch
from bots.tools.parse.parse_perplexity_question import ParsePerplexityQuestion
from bots.tools.parse.parse_user import ParseUser
from bots.tools.parse.select_random_user import SelectRandomUser


PARSE_TOOLS = [
  ParseCategory,
  ParseChannel,
  ParseKeywordAndSearch,
  ParseMoreLikeThisText,
  ParseNewsSearch,
  ParsePerplexityQuestion,
  ParseUser,
  SelectRandomUser
]