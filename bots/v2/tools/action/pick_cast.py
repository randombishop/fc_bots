from bots.i_action_step import IActionStep
from bots.prompts.format_casts import concat_casts
from bots.utils.llms import call_llm, get_max_capactity
from bots.utils.read_params import read_category, read_channel, read_user, read_keyword, read_string
from bots.data.casts import get_top_casts, get_more_like_this
from bots.utils.check_links import check_link_data


parse_instructions_template = """
INSTRUCTIONS:
You are @{{name}}, a bot programmed to select the best posts (=casts) in a social media platform.
You have access to an API that can pick the best post based on these parameters: 
category, channel, keyword, more_like_this, user, search, criteria.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* search: If the scope is not about a category, channel, keyword or user; then formulate a search phrase to search for posts and pick one.
* user: User names typically start with `@`, if the intent is to pick one post by a specific user, you can use the user parameter.
* criteria: Which criteria should be used to pick the best post? Can be any free text like 'beautiful', 'funniest', 'best', 'most informative'. Defaults to 'most interesting'.
Your goal is not to continue the conversation, you must only extract the parameters to call the API.
You can use the conversation to guess the parameters, but focus on the request.
Your goal is to extract the parameters from the request.

#CURRENT CHANNEL
{{selected_channel}}

RESPONSE FORMAT:
{
  "category": ...,
  "channel": ...,
  "keyword": "...",
  "search": "...",
  "user": "..."
  "criteria": ...
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "category":{"type":"STRING"},
    "channel":{"type":"STRING"},
    "keyword":{"type":"STRING"},
    "search":{"type":"STRING"},
    "user":{"type":"STRING"},
    "criteria":{"type":"STRING"}
  }
}


task_instructions_intro_template = """
You are @{{name}}, a bot programmed to pick the best post (=cast) in a social media platform.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#CURRENT CHANNEL
{{selected_channel}}
"""

task_instructions = """
INSTRUCTIONS:
Select the best post from this list above using this criteria: ?
Comment about the post with a keyword and emoji.
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
Focus on posts that are genuine, interesting, funny, or informative.

RESPONSE FORMAT:
{
  "id": "selected post id",
  "comment": "comment on the post with a keyword and emoji",
}
"""

task_schema = {
  "type":"OBJECT",
  "properties":{
    "id":{"type":"STRING"}, 
    "comment":{"type":"STRING"}
  }
}


class PickCast(IActionStep):

  def get_cost(self):
    return 20
  
  def parse(self):
    parse_prompt = self.state.format_conversation()
    parse_instructions = self.state.format(parse_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_schema)
    parsed = {}
    parsed['channel'] = read_channel(params)
    parsed['keyword'] = read_keyword(params)
    parsed['category'] = read_category(params)
    parsed['search'] = read_string(params, key='search', default=None, max_length=500)
    _, parsed['user_name'] = read_user(params, fid_origin=self.state.fid_origin, default_to_origin=False)
    parsed['criteria'] = read_string(params, key='criteria', default='most interesting')
    parsed['max_rows'] = get_max_capactity()
    self.state.action_params = parsed
    
  def execute(self):
    params = self.state.action_params
    posts = []
    if params['search'] is not None:
      posts = get_more_like_this(params['search'], limit=params['max_rows'])
    else:
      posts = get_top_casts(channel=params['channel'],
                            keyword=params['keyword'],
                            category=params['category'],
                            user_name=params['user_name'],
                            max_rows=params['max_rows'])
    posts = posts.to_dict('records')
    if len(posts) < 5:
      raise Exception(f"Not enough posts to pick a winner ({len(posts)} posts)")
    prompt = concat_casts(posts)
    instructions = self.state.format(task_instructions_intro_template)
    instructions += task_instructions.replace('?', params['criteria'])
    result = call_llm(prompt, instructions, task_schema)
    posts_map = {x['id']: x for x in posts}
    data = check_link_data(result, posts_map)
    cast = {
      'text': data['comment'],
      'embeds': [{'fid': data['fid'], 'user_name': data['user_name'], 'hash': data['hash']}],
      'embeds_description': data['text']
    }
    casts = [cast]
    self.state.casts = casts

