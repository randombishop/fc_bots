from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_keyword, read_category, read_string
from bots.data.casts import get_top_casts, get_more_like_this
from bots.prompts.format_casts import concat_casts


instructions_template = """
You are @{{name}}, a social media bot.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#CURRENT CHANNEL
{{selected_channel}}

#TASK
Before responding to the user, you can access data from the social media platform to come up with a better response and reference relevant posts.
You have access to an API that can pull data based on these parameters: category, keyword, search.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* keyword: Can be any single keyword.
* search: Can be any search phrase to search for posts.
Your goal is not to continue the conversation, you must only come up with interesting parameters to call the API.
Your goal is to propose parameters to gain access to more data before responding.

#RESPONSE FORMAT
{
  "category": "...",
  "keyword": "...",
  "search": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "category":{"type":"STRING"},
    "keyword":{"type":"STRING"},
    "search":{"type":"STRING"}
  }
}


def get_casts(input):
  state = input.state
  llm = input.llm
  if not state.should_continue:
    return {'log': 'Not fetching data because should_continue is false'}
  max_rows = 25
  prompt = state.format_conversation()
  instructions = state.format(instructions_template)
  params = call_llm(llm, prompt, instructions, schema)
  parsed = {}
  parsed['keyword'] = read_keyword(params)
  parsed['category'] = read_category(params)
  parsed['search'] = read_string(params, key='search', default=None, max_length=500)
  posts = []
  if state.user_origin is not None:
    posts_about_user = get_top_casts(user_name=state.user_origin, max_rows=max_rows)
    if posts_about_user is not None and len(posts_about_user) > 0:
      posts_about_user = posts_about_user.to_dict('records')
      posts_about_user.sort(key=lambda x: x['timestamp'])
      state.about_user = concat_casts(posts_about_user)
      posts += posts_about_user
  if parsed['keyword'] is not None:
    posts_about_keyword = get_top_casts(keyword=parsed['keyword'], max_rows=max_rows)
    if posts_about_keyword is not None and len(posts_about_keyword) > 0:
      posts_about_keyword = posts_about_keyword.to_dict('records')
      posts_about_keyword.sort(key=lambda x: x['timestamp'])
      state.keyword = parsed['keyword']
      state.about_keyword = concat_casts(posts_about_keyword)
      posts += posts_about_keyword
  if parsed['category'] is not None:
    posts_about_topic = get_top_casts(category=parsed['category'], max_rows=max_rows)
    if posts_about_topic is not None and len(posts_about_topic) > 0:
      posts_about_topic = posts_about_topic.to_dict('records')
      posts_about_topic.sort(key=lambda x: x['timestamp'])
      state.topic = parsed['category']
      state.about_topic = concat_casts(posts_about_topic)
      posts += posts_about_topic
  if parsed['search'] is not None:
    posts_about_context = get_more_like_this(parsed['search'], limit=max_rows)
    if posts_about_context is not None and len(posts_about_context) > 0:
      posts_about_context = posts_about_context.to_dict('records')
      posts_about_context.sort(key=lambda x: x['timestamp'])
      state.context = parsed['search']
      state.about_context = concat_casts(posts_about_context)
      posts += posts_about_context
  for p in posts:
    state.posts_map[p['id']] = p
  return {
    'user_origin': state.user_origin,
    'about_user': state.about_user, 
    'keyword': state.keyword,
    'about_keyword': state.about_keyword, 
    'topic': state.topic,
    'about_topic': state.about_topic, 
    'context': state.context,
    'about_context': state.about_context
  }


GetCasts = Tool(
  name="get_casts",
  func=get_casts,
  description="Get casts from the current user or related to the conversation in general to build up context"
)