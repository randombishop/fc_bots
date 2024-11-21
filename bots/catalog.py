# Casts functions
from bots.actions.digest_casts import DigestCasts
from bots.actions.pick_cast import PickCast
# User functions
from bots.actions.favorite_users import FavoriteUsers
from bots.actions.most_active_users import MostActiveUsers
from bots.actions.word_cloud import WordCloud
from bots.actions.psycho import Psycho
from bots.actions.roast import Roast
# Generic functions
from bots.actions.chat import Chat


ACTIONS = {
  'Summary': DigestCasts,
  'Pick': PickCast,
  'FavoriteUsers': FavoriteUsers,
  'MostActiveUsers': MostActiveUsers,
  'WordCloud': WordCloud, 
  'Psycho': Psycho,
  'Roast': Roast,
  'Chat': Chat
}


DESCRIPTIONS = """
Summary: Make a summary about posts.
Pick: Pick a post given some criteria.
FavoriteUsers: Find the favorite accounts of a user.
MostActiveUsers: List the most active users in a channel.
WordCloud: Make a word cloud of a user's posts and reactions.
Psycho: Generate a psychoanalysis for a user.
Roast: Generate a roast for a user.
Chat: General chat when no specific action can be associated with the query.
"""
