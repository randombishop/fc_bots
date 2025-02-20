from bots.i_prepare_step import IPrepareStep
from bots.utils.llms import call_llm
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
{{channel}}

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


class GetCasts(IPrepareStep):
    
  def prepare(self):
    if not self.state.should_continue:
      return
    max_rows = 25
    prompt = self.state.format_conversation()
    instructions = self.state.format(instructions_template)
    params = call_llm(prompt, instructions, schema)
    parsed = {}
    parsed['keyword'] = read_keyword(params)
    parsed['category'] = read_category(params)
    parsed['search'] = read_string(params, key='search', default=None, max_length=500)
    posts = []
    if self.state.user_origin is not None:
      posts_about_user = get_top_casts(user_name=self.state.user_origin, max_rows=max_rows)
      if posts_about_user is not None and len(posts_about_user) > 0:
        posts_about_user = posts_about_user.to_dict('records')
        posts_about_user.sort(key=lambda x: x['timestamp'])
        self.state.about_user = concat_casts(posts_about_user)
        posts += posts_about_user
    if parsed['keyword'] is not None:
      posts_about_keyword = get_top_casts(keyword=parsed['keyword'], max_rows=max_rows)
      if posts_about_keyword is not None and len(posts_about_keyword) > 0:
        posts_about_keyword = posts_about_keyword.to_dict('records')
        posts_about_keyword.sort(key=lambda x: x['timestamp'])
        self.state.keyword = parsed['keyword']
        self.state.about_keyword = concat_casts(posts_about_keyword)
        posts += posts_about_keyword
    if parsed['category'] is not None:
      posts_about_topic = get_top_casts(category=parsed['category'], max_rows=max_rows)
      if posts_about_topic is not None and len(posts_about_topic) > 0:
        posts_about_topic = posts_about_topic.to_dict('records')
        posts_about_topic.sort(key=lambda x: x['timestamp'])
        self.state.topic = parsed['category']
        self.state.about_topic = concat_casts(posts_about_topic)
        posts += posts_about_topic
    if parsed['search'] is not None:
      posts_about_context = get_more_like_this(parsed['search'], limit=max_rows)
      if posts_about_context is not None and len(posts_about_context) > 0:
        posts_about_context = posts_about_context.to_dict('records')
        posts_about_context.sort(key=lambda x: x['timestamp'])
        self.state.context = parsed['search']
        self.state.about_context = concat_casts(posts_about_context)
        posts += posts_about_context
    for p in posts:
      self.state.posts_map[p['id']] = p
