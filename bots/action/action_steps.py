from bots.action.chat import Chat
from bots.action.digest_casts import DigestCasts
from bots.action.favorite_users import FavoriteUsers
from bots.action.more_like_this import MoreLikeThis
from bots.action.most_active_users import MostActiveUsers
from bots.action.news import News
from bots.action.perplexity import Perplexity
from bots.action.pick_cast import PickCast
from bots.action.praise import Praise
from bots.action.psycho import Psycho
from bots.action.roast import Roast
from bots.action.say_something_in_channel import SaySomethingInChannel
from bots.action.say_something_no_channel import SaySomethingNoChannel
from bots.action.who_is import WhoIs
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
  'Praise': Praise,
  'Psycho': Psycho,
  'Roast': Roast,
  'SaySomethingNoChannel': SaySomethingNoChannel,
  'SaySomethingInChannel': SaySomethingInChannel,
  'WhoIs': WhoIs,
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
  'Praise': 'Generate a praise for a user.',
  'Roast': 'Generate a roast for a user.',
  'WhoIs': 'Analyze a user profile and generate a new avatar for them. (Who is @user? Make an avater for @user, Analyze user profile @user, etc.)',
  'WordCloud': 'Make a word cloud.'
}

TEMPLATES = {
  'Summary': "Summarize category {[arts, business, crypto, culture, money, nature, politics, sports, tech_science]} / Summarize channel /{channel} / Summarize posts about {search phrase} / Summarize posts by {user} / Summarize posts with keyword {keyword}",
  'MostActiveUsers': 'Most active users in /{channel}',
  'News': 'Check the news for {search phrase}',
  'Perplexity': 'Ask Perplexity ""{question}"',
  'Pick': 'Pick the {adjective} post in category {[arts, business, crypto, culture, money, nature, politics, sports, tech_science}] / Pick the {adjective} post in channel /{channel} / Pick the {adjective} post about {search phrase} / Pick the {adjective} post by {username} / Pick the {adjective} post with keyword {keyword}',
  'Psycho': 'Psycho analyze {user}',
  'Praise': 'Praise {user}',
  'Roast': 'Roast {user}',
}