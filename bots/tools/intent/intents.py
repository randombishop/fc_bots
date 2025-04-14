import random

INTENTS_DESCRIPTIONS = {
'FavoriteUsers': 'Find the favorite accounts of a user.',
'MoreLikeThis': 'Find posts using "More Like This" algorithm.',
'MostActiveUsers': 'List the most active users in a channel.',
'News': 'Check the news.',
'Perplexity': 'Ask a question to Perplexity AI.',
'Pick': 'Pick a post given some criteria.',
'Praise': 'Generate a praise for a user.',
'Psycho': 'Generate a friendly and parody psychoanalysis for a user.',
'Roast': 'Generate a friendly roast for a user.',
'Summary': 'Make a summary about posts.',
'WhoIs': 'Analyze a user profile and generate a new avatar for them.',
'WordCloud': 'Make a word cloud.',
'UserStats': 'Get users aggregation or statistic from the database.'
}

INTENTS_TARGETS = {
  
'FavoriteUsers': ['RenderFavoriteUsersTable'],

'MoreLikeThis': ['GetMoreLikeThis', 'CreateWordCloud'],

'MostActiveUsers': ['CreateMostActiveUsersChart'],

'News': ['GetNews'],

'Perplexity': ['CallPerplexity'],

'Pick': ['AggregateCasts'],

'Praise': ['CreateAvatar'],

'Psycho': ['CreateAvatar'],

'Roast': ['CreateAvatar'],

'Summary': ['CreateWordCloud'],

'WhoIs':  ['CreateAvatar'],

'WordCloud': ['CreateWordCloud'],

'UserStats': ['GetUserStats']


}



INTENTS_RESPONSE_PLANS = {
  
'FavoriteUsers': """Post one tweet about who the user likes and why.
Embed the table url in embed_url1""",
  
'MoreLikeThis': """Use the first tweet for a freestyle intro (with or without an embed, a wordcloud or anything else) 
then fill embed_hash2 and embed_hash3 with similar posts ids.""",

'MostActiveUsers': """Post one tweet about the most active users in the channel and embed the chart image in embed_url1""",

'News': """Post one tweet about the news and embed the link in embed_url1""",

'Perplexity': """Rephrase the answer from perplexity in your words in one engaging tweetand embed the link in embed_url1""",

'Pick': """Pick a post and comment it.
Make sure you fill embed_hash1 to embed the post that you picked.""",  

'Praise': """Analyze the user posts carefully.
Based on the provided information, identify their core personality and what makes them unique.
Praise them in a way that is authentic and specific, not vague.
Be yourself and include what you really like about them.
Keep it short but impactful, a poetic appreciation, a clever compliment, or a deep truth about them.
Also, embed the user's avatar in embed_url1""",

'Psycho': """Based on the posts, provide a hilariously original psychoanalysis of the user's personality in 3 tweets.
Do not use real pathology names, instead, create your own funny medical names with novel issues.
You can mix your psycho analysis with roasting.
Examine the recurring themes and word choices and explain their subconscious motivations in a playful, tongue-in-cheek manner. 
Imagine a blend of Freudian insights and stand-up comedy.
Remember to be creative, original, and thoroughly entertaining but always remain respectful.
Be respectful, and do not use sexual, religious or political references.
Also, embed the user's avatar in embed_url1""",

'Roast': """Analyze the user's posts and craft a roast that is both hilarious and original.
Roast them as hard as you can in one short but explosive tweet.
Cleverly highlight the quirky, absurd, or contradictory elements in the posts.
Use wordplay, irony, and playful sarcasm.
Maintain a humorous, light-hearted tone without resorting to unnecessarily mean-spirited personal attacks.
Be respectful, and do not use sexual, religious or political references.
Also, embed the user's avatar in embed_url1""",

'Summary': """Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
Focus on posts that are genuine, interesting, funny, or informative.
Don't reference websites and don't include any urls in your summary.
Post your summary intro and embed the wordcloud in the first tweet.
Then continue your summary in tweet2 and tweet3 and include links to the most interesting posts in embed_hash2 and embed_hash3.
""",

'WhoIs': """Analyze the user posts carefully and post a short description in one single tweet.
Embed the user's avatar in embed_url1""",

'WordCloud': """Write a word play using the most common words (wordcloud_text) and the theme from the provided posts.
Post it as a single short tweet and embed the wordcloud URL in embed_url1""",

'UserStats': """Compose a data driven response."""

}


DEFAULT_RESPONSE_PLAN = """
For your information, in the farcaster social media platform, posts are called casts.
You can optionally embed an url or a post hash if it is relevant. 
When you want to embed an url or post, use the embed_url or embed_hash fields, don't include the link or post id in the tweet field itself.
"""


def get_intents():
  return list(INTENTS_DESCRIPTIONS.keys())

def get_intents_descriptions():
  keys = list(INTENTS_DESCRIPTIONS.keys())
  random.shuffle(keys)
  ans = ''
  for key in keys:
    ans += f'{key}: {INTENTS_DESCRIPTIONS[key]}\n'
  return ans

def get_intended_targets(intent):
  return INTENTS_TARGETS[intent] if intent is not None and intent in INTENTS_TARGETS else []

def get_response_plan(intent):
  return INTENTS_RESPONSE_PLANS[intent] if intent is not None and intent in INTENTS_RESPONSE_PLANS else DEFAULT_RESPONSE_PLAN
  






#def get_intent_examples():
#  examples = ''
#  for key in get_intents():
#    examples += f'Example: {INTENTS_DESCRIPTIONS[key]}\n'
#    examples += f'> intent:\n{key}\n'
#    examples += f'> action_plan:\n{ACTION_PLANS[key]}\n'
#    examples += f'> response _plan:\n{RESPONSE_PLANS[key]}\n'
#    examples += '\n'
#  return examples