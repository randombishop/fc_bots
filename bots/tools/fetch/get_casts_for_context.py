from langchain.agents import Tool
from bots.data.casts import get_top_casts, get_more_like_this
from bots.utils.format_cast import concat_casts


def get_casts_for_context(input):
  state = input.state
  if not state.should_continue:
    return {'log': 'Not fetching data because should_continue is false'}
  posts = []
  if state.user_origin is not None:
    posts_about_user = get_top_casts(user_name=state.user_origin, max_rows=state.max_rows)
    if posts_about_user is not None and len(posts_about_user) > 0:
      posts_about_user = posts_about_user.to_dict('records')
      posts_about_user.sort(key=lambda x: x['timestamp'])
      state.about_user = concat_casts(posts_about_user)
      posts += posts_about_user
  if state.keyword is not None:
    posts_about_keyword = get_top_casts(keyword=state.keyword, max_rows=state.max_rows)
    if posts_about_keyword is not None and len(posts_about_keyword) > 0:
      posts_about_keyword = posts_about_keyword.to_dict('records')
      posts_about_keyword.sort(key=lambda x: x['timestamp'])
      state.about_keyword = concat_casts(posts_about_keyword)
      posts += posts_about_keyword
  if state.category is not None:
    posts_about_topic = get_top_casts(category=state.category, max_rows=state.max_rows)
    if posts_about_topic is not None and len(posts_about_topic) > 0:
      posts_about_topic = posts_about_topic.to_dict('records')
      posts_about_topic.sort(key=lambda x: x['timestamp'])
      state.about_category = concat_casts(posts_about_topic)
      posts += posts_about_topic
  if state.search is not None:
    posts_about_context = get_more_like_this(state.search, limit=state.max_rows)
    if posts_about_context is not None and len(posts_about_context) > 0:
      posts_about_context = posts_about_context.to_dict('records')
      posts_about_context.sort(key=lambda x: x['timestamp'])
      state.about_search = concat_casts(posts_about_context)
      posts += posts_about_context
  for p in posts:
    state.posts_map[p['id']] = p
  return {
    'user_origin': state.user_origin,
    'about_user': state.about_user, 
    'keyword': state.keyword,
    'about_keyword': state.about_keyword, 
    'category': state.category,
    'about_category': state.about_category, 
    'search': state.search,
    'about_search': state.about_search
  }


GetCastsForContext = Tool(
  name="GetCastsForContext",
  func=get_casts_for_context,
  description="Get casts from the current user or related to the conversation in general to build up context"
)