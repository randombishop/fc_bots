from dotenv import load_dotenv
load_dotenv()
import sys
from bots.iaction import IAction
from bots.utils.prompts import concat_casts
from bots.utils.llms import call_llm, get_max_capactity
from bots.utils.read_params import read_category, read_channel, read_int, read_keyword, read_string
from bots.data.casts import get_top_casts
from bots.utils.check_links import check_link_data
from bots.utils.check_casts import check_casts


parse_instructions = """
INSTRUCTIONS:
Find and extract following parameters from the user input: channel, category, and criteria.
Your goal is not to answer the user query, you only need to extract the parameters.
The query doesn't need to match a specific format, your job is to guess the parameters that the user is asking for.

EXAMPLES:
* get me the funniest cast in /ted channel -> criteria=funniest, channel=/ted,
* Best of arts -> criteria=best, category=arts

PARAMETERS
* category, optional, one of pre-defined categories, defaults to null. Allowed categories are: 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel, optional, defaults to null. (channels always start with '/', for example '/data', if there is no '/' then it's not a channel)
* criteria is free text and defaults to 'most interesting'

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
    "channel":{"type":"STRING"},
    "category":{"type":"STRING"},
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
    self.category = read_category(params)
    self.criteria = read_string(params, 'criteria', 'most interesting', 100)
    self.max_rows = get_max_capactity()
    
  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    posts = get_top_casts(channel=self.channel,
                          keyword=None,
                          category=self.category,
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

