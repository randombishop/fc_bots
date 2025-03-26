from langchain.agents import Tool
from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.compose import COMPOSE_TOOLS


TOOL_LIST = PARSE_TOOLS + FETCH_TOOLS + PREPARE_TOOLS + COMPOSE_TOOLS
TOOL_MAP = {t.name: t for t in TOOL_LIST}


ACTION_CONFIG = {
  'Chat': {
    'parse': ['ParseContextParams'],
    'fetch': ['GetCastsForContext'],
    'compose': ['ComposeChat']
  },
  'Summary': {
    'parse': ['ParseSummaryParams'],
    'fetch': ['GetCastsForParams'],
    'prepare': ['PrepareSummary', 'GenerateWordCloud'],
    'compose': ['ComposeSummary']
  },
  'FavoriteUsers': {
    'parse': ['ParseFavoriteUsersParams'],
    'fetch': ['GetFavoriteUsers'],
    'prepare': ['PrepareFavoriteUsersTable'],
    'compose': ['ComposeFavoriteUsers']
  },
  'MoreLikeThis': {
    'parse': ['ParseMoreLikeThisParams'],
    'fetch': ['GetMoreLikeThis'],
    'compose': ['ComposeMoreLikeThis']
  },
  'MostActiveUsers': {
    'parse': ['ParseMostActiveUsersParams'],
    'fetch': ['GetMostActiveUsers'],
    'prepare': ['PrepareMostActiveUsersChart'],
    'compose': ['ComposeMostActiveUsers']
  },
  'Pick': {
    'parse': ['ParsePickParams'],
    'fetch': ['GetCastsForParams'],
    'compose': ['ComposePick']
  },
  'WordCloud': {
    'parse': ['ParseWordCloudParams'],
    'fetch': ['GetCastsForParams'],
    'prepare': ['PrepareWordCloud', 'GenerateWordCloud'],
    'compose': ['ComposeWordCloud']
  },
  'Psycho': {
    'parse': ['ParsePsychoParams'],
    'fetch': ['GetCastsForFid'],
    'prepare': ['PreparePsycho'],
    'compose': ['ComposePsycho']
  },
  'Roast': {
    'parse': ['ParseRoastParams'],
    'fetch': ['GetCastsForFid'],
    'prepare': ['PrepareRoast'],
    'compose': ['ComposeRoast']
  },
  'Perplexity': {
    'parse': ['ParsePerplexityParams'],
    'prepare': ['CallPerplexity'],
    'compose': ['ComposePerplexity']
  },
  'News': {
    'parse': ['ParseNewsParams'],
    'fetch': ['GetNews'],
    'compose': ['ComposeNews']
  },
  'WhoIs': {
    'parse': ['ParseWhoIsParams'],
    'fetch': ['GetUserProfile', 'GetUserRepliesAndReactions'],
    'prepare': ['DescribePfp', 'DescribeUserCasts', 'DescribeUserRepliesAndReactions', 'GenerateAvatar'],
    'compose': ['ComposeWhoIs']
  },
  'Praise': {
    'parse': ['ParsePraiseParams'],
    'fetch': ['GetUserProfile', 'GetUserRepliesAndReactions'],
    'prepare': ['DescribePfp', 'DescribeUserCasts', 'DescribeUserRepliesAndReactions', 'GenerateAvatar', 'PreparePraise'],
    'compose': ['ComposePraise']
  }
}


def bot_action(input):
  action = input.state.action
  if action is None or action not in ACTION_CONFIG:
    return {'log': 'No configured action'}
  action_config = ACTION_CONFIG[action]
  sequence = []
  for phase in action_config:
    sequence += action_config[phase]
  for tool_name in sequence:
    tool = TOOL_MAP[tool_name]
    tool.invoke({'input': input})
  return {'sequence': sequence}


BotAction = Tool(
  name="BotAction",
  description="Bot action phase",
  func=bot_action
)