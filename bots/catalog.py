# Casts functions
from bots.actions.digest_casts import DigestCasts
from bots.actions.pick_cast import PickCast
from bots.actions.more_like_this import MoreLikeThis
# User functions
from bots.actions.favorite_users import FavoriteUsers
from bots.actions.most_active_users import MostActiveUsers
from bots.actions.word_cloud import WordCloud
from bots.actions.psycho import Psycho
from bots.actions.roast import Roast
from bots.actions.perplexity import Perplexity
from bots.actions.news import News


ACTIONS = {
  'Summary': DigestCasts,
  'Pick': PickCast,
  'MoreLikeThis': MoreLikeThis,
  'FavoriteUsers': FavoriteUsers,
  'MostActiveUsers': MostActiveUsers,
  'WordCloud': WordCloud, 
  'Psycho': Psycho,
  'Roast': Roast,
  'Perplexity': Perplexity,
  'News': News
}


DESCRIPTIONS = """
Summary: Make a summary about posts.
Pick: Pick a post given some criteria.
MoreLikeThis: Find posts using "More Like This" algorithm.
FavoriteUsers: Find the favorite accounts of a user.
MostActiveUsers: List the most active users in a channel.
WordCloud: Make a word cloud of a user's posts and reactions.
Psycho: Generate a psychoanalysis for a user.
Roast: Generate a roast for a user.
Perplexity: Ask a question to Perplexity AI.
News: Check the news with a search query.
"""
