from bots.tools.prepare.call_perplexity import CallPerplexity
from bots.tools.prepare.create_avatar import CreateAvatar
from bots.tools.prepare.create_most_active_users_chart import CreateMostActiveUsersChart
from bots.tools.prepare.create_wordcloud import CreateWordCloud
from bots.tools.prepare.describe_pfp import DescribePfp
from bots.tools.prepare.describe_user_casts import DescribeUserCasts
from bots.tools.prepare.describe_user_replies_and_reactions import DescribeUserRepliesAndReactions
from bots.tools.prepare.prepare_praise import PreparePraise
from bots.tools.prepare.prepare_psycho import PreparePsycho
from bots.tools.prepare.prepare_roast import PrepareRoast
from bots.tools.prepare.prepare_summary import PrepareSummary
from bots.tools.prepare.render_favorite_users_table import RenderFavoriteUsersTable


PREPARE_TOOLS = [
  CallPerplexity,
  CreateAvatar,
  CreateMostActiveUsersChart,
  CreateWordCloud,
  DescribePfp,
  DescribeUserCasts,
  DescribeUserRepliesAndReactions,
  PreparePraise,
  PreparePsycho,
  PrepareRoast,
  PrepareSummary,
  RenderFavoriteUsersTable
]