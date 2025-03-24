ACTION_DESCRIPTIONS = {
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


ACTION_TEMPLATES = {
  'Summary': "Summarize category {[arts, business, crypto, culture, money, nature, politics, sports, tech_science]} / Summarize channel /{channel} / Summarize posts about {search phrase} / Summarize posts by {user} / Summarize posts with keyword {keyword}",
  'MostActiveUsers': 'Most active users in /{channel}',
  'News': 'Check the news for {search phrase}',
  'Perplexity': 'Ask Perplexity ""{question}"',
  'Pick': 'Pick the {adjective} post in category {[arts, business, crypto, culture, money, nature, politics, sports, tech_science}] / Pick the {adjective} post in channel /{channel} / Pick the {adjective} post about {search phrase} / Pick the {adjective} post by {username} / Pick the {adjective} post with keyword {keyword}',
  'Psycho': 'Psycho analyze {user}',
  'Praise': 'Praise {user}',
  'Roast': 'Roast {user}',
}


ACTION_CONFIG = {
  'Chat': {
    'compose': ['ComposeChat']
  },
  'Summary': {
    'parse': ['ParseSummaryParams'],
    'fetch': ['GetCastsForParams'],
    'prepare': ['PrepareSummary', 'GenerateWordCloudMask', 'GenerateWordCloud'],
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
    'prepare': ['PrepareWordCloud', 'GenerateWordCloudMask', 'GenerateWordCloud'],
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
    'compose': ['ComposeWhoIs'],
    'memorize': ['SaveUserProfile']
  },
  'Praise': {
    'parse': ['ParsePraiseParams'],
    'fetch': ['GetUserProfile', 'GetUserRepliesAndReactions'],
    'prepare': ['DescribePfp', 'DescribeUserCasts', 'DescribeUserRepliesAndReactions', 'GenerateAvatar', 'PreparePraise'],
    'compose': ['ComposePraise'],
    'memorize': ['SaveUserProfile']
  }
}


