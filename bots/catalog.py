# Casts functions
from bots.actions.digest_casts import DigestCasts
from bots.actions.pick_cast import PickCast
# User functions
from bots.actions.favorite_users import FavoriteUsers
from bots.actions.most_active_users import MostActiveUsers
from bots.actions.prefs_cloud import PrefsCloud
from bots.actions.psycho import Psycho
from bots.actions.roast import Roast
# Generic functions
from bots.actions.run_sql import RunSql
from bots.actions.chat import Chat


ACTIONS = {
  10: DigestCasts,
  11: PickCast,

  21: FavoriteUsers,
  22: MostActiveUsers,
  23: PrefsCloud, 
  24: Psycho,
  25: Roast,

  91: RunSql,
  92: Chat
}


DESCRIPTIONS = """

# LIST OF ACTIONS

## Queries about posts
10. Summarizes posts by channel, keywords, or topic.
11. Picks the best post from a channel or by keywords. (Can use custom criteria.)

## Queries about users
21. Finds the favorite accounts of a user.
22. Lists the most active users in a channel or by keywords.
23. Make a word cloud of a user's posts and reactions.
24. Generate a psychoanalysis for a user.
25. Generate a roast for a user.

## Generic queries
91. Runs a SQL query. (Query must be a valid SQL query, do not try to convert the user query from natural language to SQL.)
92. Responds in natural language. Uses a LLM to generate an answer.

"""
