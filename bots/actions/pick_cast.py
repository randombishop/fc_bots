from dotenv import load_dotenv
load_dotenv()
import sys
from bots.iaction import IAction
from bots.utils.prompts import concat_casts
from bots.utils.llms import call_llm, get_max_capactity
from bots.utils.read_params import read_category, read_channel, read_user_name, read_keyword, read_string
from bots.data.casts import get_top_casts, get_more_like_this
from bots.utils.check_links import check_link_data
from bots.utils.check_casts import check_casts


parse_instructions = """
INSTRUCTIONS:
You are @dsart, a bot programmed to select the best posts (=casts) in a social media platform.
You have access to an API that can pick the best post based on these parameters: 
category, channel, keyword, more_like_this, user, search, criteria.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* user: User names typically start with `@`, if the intent is to pick one post by a specific user, you can use the user parameter.
* search: If the scope is not about a category, channel, keyword or user; then formulate a search phrase to search for posts and pick one.
* criteria: Which criteria should be used to pick the best post? Can be any free text like 'beautiful', 'funniest', 'best', 'most informative'. Defaults to 'most interesting'.
Your goal is not to continue the conversation directly, you must only need to extract the parameters to call the API.

RESPONSE FORMAT:
{
  "category": ...,
  "channel": ...,
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



task_instructions = """
INSTRUCTIONS:
  - Select the best post from this list above using this criteria: ?
  - Comment about the post with a keyword and emoji.
  - Output the result in json format.
  - Make sure you don't use " inside json strings. Avoid invalid json.
  - Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
  - Focus on posts that are genuine, interesting, funny, or informative.

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


class PickCast(IAction):

  def set_input(self, input):
    params = call_llm(input, parse_instructions, parse_schema)
    self.input = input
    self.set_params(params)
    
  def set_params(self, params):
    self.channel = read_channel(params)
    self.keyword = read_keyword(params)
    self.category = read_category(params)
    self.search = read_string(params, key='search', default=None, max_length=500)
    self.user_name = read_user_name(params, fid_origin=self.fid_origin, default_to_origin=False)
    self.criteria = read_string(params, key='criteria', default='most interesting')
    self.max_rows = get_max_capactity()
    
  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    posts = []
    if self.search is not None:
      posts = get_more_like_this(self.search, limit=self.max_rows)
    else:
      posts = get_top_casts(channel=self.channel,
                            keyword=self.keyword,
                            category=self.category,
                            user_name=self.user_name,
                            max_rows=self.max_rows)
    posts = posts.to_dict('records')
    if len(posts) < 5:
      raise Exception(f"Not enough posts to pick a winner ({len(posts)} posts)")
    prompt = concat_casts(posts)
    result = call_llm(prompt, task_instructions.replace('?', self.criteria), task_schema)
    posts_map = {x['id']: x for x in posts}
    result = check_link_data(result, posts_map)
    self.data = result
    return result
    
  def get_casts(self, intro=''):
    casts = []
    cast = {
      'text': self.data['comment'],
      'embeds': [{'fid': self.data['fid'], 'user_name': self.data['user_name'], 'hash': self.data['hash']}]
    }
    casts.append(cast)
    check_casts(casts)
    self.casts = casts
    return self.casts

