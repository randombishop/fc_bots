import random
from bots.kit_interface.capabilities_examples import CapabilitiesExamples


INTENTS_DESCRIPTIONS = {
'FavoriteUsers': 'Find the favorite accounts of a user.',
'MoreLikeThis': 'Find posts using "More Like This" algorithm.',
'MostActiveUsers': 'List the most active users in a channel.',
'News': 'Check the news.',
'Pick': 'Pick a post given some criteria.',
'Praise': 'Generate a praise for a user.',
'Psycho': 'Generate a friendly and parody psychoanalysis for a user.',
'Roast': 'Generate a friendly roast for a user.',
'Summary': 'Make a summary about posts.',
'WhoIs': 'Analyze a user profile and generate a new avatar for them.',
'WordCloud': 'Make a word cloud.',
'UserStats': 'Get users aggregation or statistic from the database.',
'CastStats': 'Get casts (=posts) aggregation or statistic from the database.',
'Meta': 'Explain what the bot can do and how to use it.'
}


INTENTS_RESPONSE_PLANS = {
  
'FavoriteUsers': """Fetch favorite users data.
Prepare favorite users table.
Post about who the user likes and include the table url.
Use the table url that you created, do not guess a link if it doesn't appear on your own data.
""",
  
'MoreLikeThis': """Prepare as search phrase and fetch similar casts.
Create a wordcloud from similar casts.
Post a thread with the wordcloud url in the first post and then links to similar posts ids in second and third posts.""",


'MostActiveUsers': """Fetch most active users data.
Prepare most active users chart.
Post about the the most active users in the channel and link to the chart url.
Use the chart url that you created, do not guess a link if it doesn't appear on your own data.
""",

'News': """Fetch the news using a relevant search phrase.
Post about the news and include the link to the story.
Use the news link you obtained, do not guess a link if it doesn't appear on your own data.""",

'Pick': """Fetch relevant casts.
Pick a cast id and comment it.
Make sure you include a link to the cast id that you picked.""",  

'Praise': """Fetch the user's profile.
Fetch the user's casts.
Create a new avatar for the user.
Based on the data, identify their core personality and what makes them unique.
Praise them in a way that is authentic and specific, not vague.
Be yourself and include what you really like about them.
Keep it short but impactful, a poetic appreciation, a clever compliment, or a deep truth about them.
Include the url to the avatar you created in the first post.
Use the avatar url that you created, do not guess a link if it doesn't appear on your own data.""",

'Psycho': """Fetch the user's profile.
Fetch the user's casts.
Create an image to illustrate your psycho analysis.
Based on their posts, provide a hilariously original psychoanalysis of the user's personality in 3 tweets.
Do not use real pathology names, instead, create your own funny medical names with novel issues.
You can mix your psycho analysis with roasting.
Examine the recurring themes and word choices and explain their subconscious motivations in a playful, tongue-in-cheek manner. 
Imagine a blend of Freudian insights and stand-up comedy.
Remember to be creative, original, and thoroughly entertaining but always remain respectful.
Be respectful, and do not use sexual, religious or political references.
Include the url link to the image you created in the first post.
Use the image url that you created, do not guess a link if it doesn't appear on your own data.""",

'Roast': """Fetch the user's profile.
Fetch the user's casts.
Create an image to illustrate your roast.
Analyze the user's posts and craft a roast that is both hilarious and original.
Roast them as hard as you can in one short but explosive tweet.
Cleverly highlight the quirky, absurd, or contradictory elements in the posts.
Use wordplay, irony, and playful sarcasm.
Maintain a humorous, light-hearted tone without resorting to unnecessarily mean-spirited personal attacks.
Be respectful, and do not use sexual, religious or political references.
Include the url link to the image you created in the first post.
Use the image url that you created, do not guess a link if it doesn't appear on your own data.""",

'Summary': """Fetch relevant casts.
Create a word cloud.
Study the posts and summarize them.
Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
Focus on posts that are genuine, interesting, funny, or informative.
You can only include urls that you generated yourself, or post ids that you carefully selected, but you can't include urls pointing to external websites.
Post your summary intro and a link to the wordcloud url that you created in the first post.
Then continue your summary in the second and third post and include links to the most interesting posts.
Use the wordcloud url that the post ids from your data as links, do not guess links or urls if they don't appear on your own data.""",

'WhoIs': """Fetch the user's profile.
Fetch the user's casts.
Create a new avatar for the user.
Analyze the user posts carefully and post a short description in one single tweet.
Include the user's avatar url link.
Use the avatar url that you created, do not guess a link if it doesn't appear on your own data.""",

'WordCloud': """Fetch relevant casts.
Create a word cloud.
Study the casts and write a word play using the most common words and the theme from the provided posts.
Post it as a single short cast and include a link to the wordcloud URL.
Use the wordcloud url that you created, do not guess a link or url if they don't appear on your own data.""",

'UserStats': """Make a SQL query to fetch user statistics from Dune Analytics.
Execute the query.
Compose a data driven response.""",

'CastStats': """Make a SQL query to fetch cast statistics from Dune Analytics.
Execute the query.
Compose a data driven response.
""",

'Meta': """Fetch examples of your capabilities.
Fetch your source code.
Study your capabilities and source code and let the user know how you can help them.
Be accurate and honest about your capabilities and avoid making false promises.
"""
}


DEFAULT_RESPONSE_PLAN = """
Use your tools to your best ability to prepare relevant data.
Use your data to compose an appropriate response.
You can optionally link to an url or a cast id if it is relevant, but do not guess links or urls if they don't appear on your own data. 
"""


def get_capabilities_examples() -> CapabilitiesExamples:
  examples = INTENTS_DESCRIPTIONS.values()
  random.shuffle(examples)
  text = '\n'.join(examples)
  return CapabilitiesExamples(text)


def get_intents():
  return list(INTENTS_DESCRIPTIONS.keys())


def get_intents_descriptions():
  keys = list(INTENTS_DESCRIPTIONS.keys())
  random.shuffle(keys)
  ans = ''
  for key in keys:
    ans += f'{key}: {INTENTS_DESCRIPTIONS[key]}\n'
  return ans


def get_response_plan(intent):
  return INTENTS_RESPONSE_PLANS[intent] if intent is not None and intent in INTENTS_RESPONSE_PLANS else DEFAULT_RESPONSE_PLAN
  

