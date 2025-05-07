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
'UserStats': 'Get users aggregation or statistic from the database.',
'CastStats': 'Get casts (=posts) aggregation or statistic from the database.'
}

INTENTS_TARGETS = {
  
'FavoriteUsers': [{'tool': 'prepare', 'method': 'render_favorite_users_table'}],

'MoreLikeThis': [{'tool': 'fetch', 'method': 'get_casts_search'}, {'tool': 'prepare', 'method': 'create_word_cloud'}],

'MostActiveUsers': [{'tool': 'prepare', 'method': 'create_most_active_users_chart'}],

'News': [{'tool': 'fetch', 'method': 'get_news'}],

'Pick': [{'tool': 'fetch', 'method': 'aggregate_casts'}],

'Praise': [{'tool': 'prepare', 'method': 'create_avatar'}],

'Psycho': [{'tool': 'prepare', 'method': 'create_avatar'}],

'Roast': [{'tool': 'prepare', 'method': 'create_avatar'}],

'Summary': [{'tool': 'prepare', 'method': 'create_word_cloud'}],

'WhoIs':  [{'tool': 'prepare', 'method': 'create_avatar'}],

'WordCloud': [{'tool': 'prepare', 'method': 'create_word_cloud'}],

'UserStats': [{'tool': 'fetch', 'method': 'make_user_stats_sql_query'}, {'tool': 'fetch', 'method': 'execute_dune_query'}],

'CastStats': [{'tool': 'fetch', 'method': 'make_cast_stats_sql_query'}, {'tool': 'fetch', 'method': 'execute_dune_query'}]

}



INTENTS_RESPONSE_PLANS = {
  
'FavoriteUsers': """Post one cast about who the user likes.
Include a link to the table url that you created.
Do not guess a table link, only use the one that you created.""",
  
'MoreLikeThis': """Use the first post for a freestyle intro (with or without an embed, a wordcloud or anything else) 
then link to similar posts ids in second and third posts.""",

'MostActiveUsers': """Post one cast about the most active users in the channel and link to the chart image""",

'News': """Post one cast about the news and include the link to the story""",

'Pick': """Pick a post and comment it.
Make sure you include a link to the post that you picked.""",  

'Praise': """Analyze the user posts carefully.
Based on the provided information, identify their core personality and what makes them unique.
Praise them in a way that is authentic and specific, not vague.
Be yourself and include what you really like about them.
Keep it short but impactful, a poetic appreciation, a clever compliment, or a deep truth about them.
Also, embed the user's avatar in the first post""",

'Psycho': """Based on the posts, provide a hilariously original psychoanalysis of the user's personality in 3 tweets.
Do not use real pathology names, instead, create your own funny medical names with novel issues.
You can mix your psycho analysis with roasting.
Examine the recurring themes and word choices and explain their subconscious motivations in a playful, tongue-in-cheek manner. 
Imagine a blend of Freudian insights and stand-up comedy.
Remember to be creative, original, and thoroughly entertaining but always remain respectful.
Be respectful, and do not use sexual, religious or political references.
Also, include a link to the user's avatar url""",

'Roast': """Analyze the user's posts and craft a roast that is both hilarious and original.
Roast them as hard as you can in one short but explosive tweet.
Cleverly highlight the quirky, absurd, or contradictory elements in the posts.
Use wordplay, irony, and playful sarcasm.
Maintain a humorous, light-hearted tone without resorting to unnecessarily mean-spirited personal attacks.
Be respectful, and do not use sexual, religious or political references.
Also, include the link to the user's avatar""",

'Summary': """Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
Focus on posts that are genuine, interesting, funny, or informative.
You can only include urls that you generated yourself, or post ids that you carefully selected, but you can't include urls pointing to external websites.
Post your summary intro and a link to the wordcloud that you created in the first post.
Then continue your summary in the second and third post and include links to the most interesting posts.
""",

'WhoIs': """Analyze the user posts carefully and post a short description in one single tweet.
Include the user's avatar url link""",

'WordCloud': """Write a word play using the most common words (wordcloud_text) and the theme from the provided posts.
Post it as a single short tweet and include a link to the wordcloud URL""",

'UserStats': """Compose a data driven response.""",

'CastStats': """Compose a data driven response."""

}


DEFAULT_RESPONSE_PLAN = """
For your information, in the farcaster social media platform, posts are called casts.
You can optionally link to an url or a post hash if it is relevant. 
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
  

