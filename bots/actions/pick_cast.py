from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.prompts import instructions_and_request, casts_and_instructions
from bots.utils.llms import call_llm
from bots.utils.read_params import read_category, read_channel, read_int, read_keywords, read_string
from bots.data.top_casts import top_casts_sql, top_casts_results
from bots.data.bq import dry_run
from bots.utils.check_links import check_link_data
from bots.utils.check_casts import check_casts


parse_instructions = """
INSTRUCTIONS:
Find and extract following parameters from the user input: channel, category, number of days, criteria.
Your goal is not to answer the user query, you only need to extract the parameters.
The query doesn't need to match a specific format, your job is to guess the parameters that the user is asking for.

EXAMPLES:
* get me the funniest cast in /ted channel last week -> criteria=funniest, channel=/ted, num_days=7
* Best of arts -> criteria=best, category=arts

PARAMETERS
* channel is an optional parameter and defaults to null
* category, optional, one of pre-defined categories, defaults to null. Allowed categories are: 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* num_days is an optional parameter and defaults to 1  
* criteria is free text and defaults to 'most interesting'

RESPONSE FORMAT:
{
  "channel": ...,
  "category": ...,
  "num_days": ...,
  "criteria": ...
}
"""


task_instructions = """
INSTRUCTIONS:
  - Select the best post from this list above using this criteria: {}
  - Comment about the post with a keyword and emoji.
  - Output the result in json format.
  - Make sure you don't use " inside json strings. Avoid invalid json.
  - Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
  - Focus on posts that are genuine, interesting, funny, or informative.

RESPONSE FORMAT:
{{
  "id": "selected post uuid",
  "text": "original text of the post",
  "comment": "comment on the post with a keyword and emoji",
}}
"""


class PickCast(IAction):

  def set_input(self, input):
    prompt = instructions_and_request(parse_instructions, input)
    params = call_llm(prompt)
    self.set_params(params)
    
  def set_params(self, params):
    self.channel = read_channel(params)
    self.category = read_category(params)
    self.criteria = read_string(params, 'criteria', 'most interesting', 100)
    self.num_days = read_int(params, 'num_days', 7, 1, 10)
    self.max_rows = 100
    
  def get_cost(self):
    sql, params = top_casts_sql(channel=self.channel, num_days=self.num_days, 
                                max_rows=self.max_rows, keywords=None, 
                                category=self.category, informative=False)
    test = dry_run(sql, params)
    self.cost = test['cost']
    return self.cost

  def get_data(self):
    posts = top_casts_results(channel=self.channel, num_days=self.num_days, 
                              max_rows=self.max_rows, keywords=None, 
                              category=self.category, informative=False)
    if len(posts) < 5:
      raise Exception(f"Not enough posts to pick a winner ({len(posts)} posts)")
    prompt = casts_and_instructions(posts, task_instructions.format(self.criteria))
    result = call_llm(prompt)
    posts_map = {x['hash']: x for x in posts}
    result = check_link_data(result, posts_map)
    self.data = result
    return result
    
  def get_casts(self, intro=''):
    casts = []
    cast = {
      'text': self.data['comment'],
      'embeds': [{'fid': self.data['fid'], 'user_name': self.data['user_name'], 'hash': self.data['id']}]
    }
    casts.append(cast)
    check_casts(casts)
    self.casts = casts
    return self.casts


if __name__ == "__main__":
  input = sys.argv[1]
  action = PickCast()
  action.set_input(input)
  print(f"Channel: {action.channel}")
  print(f"Category: {action.category}")
  print(f"Criteria: {action.criteria}")
  print(f"Num days: {action.num_days}") 
  print(f"Max rows: {action.max_rows}")
  cost = action.get_cost()
  print(f"Cost: {cost}")
  action.get_data()
  print(f"Data: {action.data}")
  action.get_casts(intro='🗞️ Channel Digest 🗞️')
  print(f"Casts: {action.casts}")
  