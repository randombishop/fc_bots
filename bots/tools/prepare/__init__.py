from bots.tools.prepare.call_perplexity import CallPerplexity
from bots.tools.prepare.describe_pfp import DescribePfp
from bots.tools.prepare.describe_user_casts import DescribeUserCasts
from bots.tools.prepare.describe_user_replies_and_reactions import DescribeUserRepliesAndReactions
from bots.tools.prepare.generate_avatar import GenerateAvatar
from bots.tools.prepare.generate_wordcloud import GenerateWordCloud
from bots.tools.prepare.prepare_favorite_users_table import PrepareFavoriteUsersTable
from bots.tools.prepare.prepare_most_active_users_chart import PrepareMostActiveUsersChart
from bots.tools.prepare.prepare_praise import PreparePraise
from bots.tools.prepare.prepare_psycho import PreparePsycho
from bots.tools.prepare.prepare_roast import PrepareRoast
from bots.tools.prepare.prepare_summary import PrepareSummary
from bots.tools.prepare.prepare_word_cloud import PrepareWordCloud


PREPARE_TOOLS = [
  CallPerplexity,
  DescribePfp,
  DescribeUserCasts,
  DescribeUserRepliesAndReactions,
  GenerateAvatar,
  GenerateWordCloud,
  PrepareFavoriteUsersTable,
  PrepareMostActiveUsersChart,
  PreparePraise,
  PreparePsycho,
  PrepareRoast,
  PrepareSummary,
  PrepareWordCloud
]