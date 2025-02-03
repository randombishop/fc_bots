from bots.action.chat import Chat
from bots.action.digest_casts import DigestCasts
from bots.action.favorite_users import FavoriteUsers
from bots.action.more_like_this import MoreLikeThis
from bots.action.most_active_users import MostActiveUsers
from bots.action.news import News
from bots.action.perplexity import Perplexity
from bots.action.pick_cast import PickCast
from bots.action.psycho import Psycho
from bots.action.roast import Roast
from bots.action.word_cloud import WordCloud


ACTION_STEPS = {
  'Chat': Chat,
  'Summary': DigestCasts,
  'FavoriteUsers': FavoriteUsers,
  'MoreLikeThis': MoreLikeThis,
  'MostActiveUsers': MostActiveUsers,
  'News': News,
  'Perplexity': Perplexity,
  'Pick': PickCast,
  'Psycho': Psycho,
  'Roast': Roast,
  'WordCloud': WordCloud
}


DESCRIPTIONS = {
  'Chat': 'Default action if no other intent is applicable.',
  'Summary': 'Make a summary about posts.',
  'FavoriteUsers': 'Find the favorite accounts of a user.',
  'MoreLikeThis': 'Find posts using "More Like This" algorithm.',
  'MostActiveUsers': 'List the most active users in a channel.',
  'News': 'Check the news.',
  'Perplexity': 'Ask a question to Perplexity AI.',
  'Pick': 'Pick a post given some criteria.',
  'Psycho': 'Generate a psychoanalysis for a user.',
  'Roast': 'Generate a roast for a user.',
  'WordCloud': 'Make a word cloud.'
}