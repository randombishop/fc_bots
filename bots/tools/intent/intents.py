import random

INTENTS_DESCRIPTIONS = {
'FavoriteUsers': 'Find the favorite accounts of a user.',
'MoreLikeThis': 'Find posts using "More Like This" algorithm.',
'MostActiveUsers': 'List the most active users in a channel.',
'News': 'Check the news.',
'Perplexity': 'Ask a question to Perplexity AI.',
'Pick': 'Pick a post given some criteria.',
'Praise': 'Generate a praise for a user.',
'Psycho': 'Generate a psychoanalysis for a user.',
'Roast': 'Generate a roast for a user.',
'Summary': 'Make a summary about posts.',
'WhoIs': 'Analyze a user profile and generate a new avatar for them.',
'WordCloud': 'Make a word cloud.'
}

ACTION_PLANS = {
  
'FavoriteUsers': """Parse the target user id 
> Get favorite users data, get the user replies and reactions 
> Render favorite users table 
> Post about what they like, tag their favorite users, and embed the table as an image""",

'MoreLikeThis': """Parse the more-like-this text 
> Fetch similar posts
> Make a wordcloud
> Post the wordcloud and embed a couple of links""",

'MostActiveUsers': """Parse the target channel
> Fetch most active users data
> Create most active users chart
> Post a banger with the chart""",

'News': """Parse the news search query
> Fetch a news story
> Make an engaging post and embed the link
""",

'Perplexity': """Parse the question 
> Call Perplexity AI.
> Reformulate the answer in your words and use the proposed link""",

'Pick': """Parse the parameter to fetch posts
> Fetch the relevant posts
> Pick one and comment it""",

'Praise': """Parse the target user id
> Fetch the user profile and the user's posts
> Generate an avatar for the user
> Post a praise with the avatar""",

'Psycho': """Parse the target user id
> Fetch the user profile and the user's posts
> Describe the user's PFP
> Write a funny psychoanalysis.""",

'Roast': """Parse the target user id
> Fetch the user profile and the user's posts
> Describe the user's PFP
> Post a roast""",

'Summary': """Parse the parameter to fetch posts to summarize
> Get posts for the parsed parameter
> Generate a wordcloud
> Post a summary, plus the wordcloud, plus links to the most interesting posts.""",

'WhoIs': """Parse the target user id
> Fetch the user profile, their posts, their replies and reactions
> Generate an avatar
> Post the avatar with a user description.""",

'WordCloud': """Parse the parameter to fetch posts
> Get posts for the parsed parameter
> Generate a wordcloud
> Post the wordcloud with a short comment"""

}



RESPONSE_PLANS = {
  
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
Keep it short but impactful, a poetic appreciation, a clever compliment, or a deep truth about them.""",

'Psycho': """Based on the posts, provide a hilariously original psychoanalysis of the user's personality in 3 tweets.
Do not use real pathology names, instead, create your own funny medical names with novel issues.
You can mix your psycho analysis with roasting.
Examine the recurring themes and word choices and explain their subconscious motivations in a playful, tongue-in-cheek manner. 
Imagine a blend of Freudian insights and stand-up comedy.
Remember to be creative, original, and thoroughly entertaining but always remain respectful.
Be respectful, and do not use sexual, religious or political references.""",

'Roast': """Analyze the user's posts and craft a roast that is both hilarious and original.
Roast them as hard as you can in one short but explosive tweet.
Cleverly highlight the quirky, absurd, or contradictory elements in the posts.
Use wordplay, irony, and playful sarcasm.
Maintain a humorous, light-hearted tone without resorting to unnecessarily mean-spirited personal attacks.
Be respectful, and do not use sexual, religious or political references.""",

'Summary': """Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
Focus on posts that are genuine, interesting, funny, or informative.
Don't reference websites and don't include any urls in your summary.
Post your summary intro and embed the wordcloud in the first tweet.
Then continue your summary in tweet2 and tweet3 and include links to the most interesting posts in embed_hash2 and embed_hash3.
""",

'WhoIs': """Analyze the user posts carefully and post a short description in one single tweet.
Embed the user's avatar in embed_url1""",

'WordCloud': """Write a word play using the most common words (wordcloud_text) and the theme from the provided posts.
Post it as a single short tweet and embed the wordcloud URL in embed_url1"""

}

DEFAULT_ACTION_PLAN = """
Parse one parameter
> Fetch relevant data
> Optionally prepare some additional media
> Compose a response
"""

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

def get_intent_examples():
  examples = ''
  for key in get_intents():
    examples += f'Example: {INTENTS_DESCRIPTIONS[key]}\n'
    examples += f'> intent:\n{key}\n'
    examples += f'> action_plan:\n{ACTION_PLANS[key]}\n'
    examples += f'> response _plan:\n{RESPONSE_PLANS[key]}\n'
    examples += '\n'
  return examples

def get_action_plan(intent):
  return ACTION_PLANS[intent] if intent is not None and intent in ACTION_PLANS else DEFAULT_ACTION_PLAN

def get_response_plan(intent):
  return RESPONSE_PLANS[intent] if intent is not None and intent in RESPONSE_PLANS else DEFAULT_RESPONSE_PLAN
  