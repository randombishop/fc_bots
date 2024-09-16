from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.prompts import instructions_and_request, casts_and_instructions
from bots.utils.llms import call_llm
from bots.utils.read_params import read_channel, read_int, read_keywords, read_string
from bots.data.top_casts import top_casts_sql, top_casts_results
from bots.data.bq import dry_run
from bots.utils.check_links import check_link_data
from bots.utils.check_casts import check_casts


parse_instructions = """
INSTRUCTIONS:
Extract the parameters from the user query to select the best post from a channel or using keyword search, 
over a number of days, using some criteria.
Your goal is not to answer the user query, you only need to extract the parameters.

PARAMETERS
* channel is an optional parameter and defaults to null
* keywords, comma separated list of keywords, optional, defaults to null
* num_days is an optional parameter and defaults to 1  
* criteria is free text and defaults to 'most interesting'

RESPONSE FORMAT:
{{
  "channel": ...,
  "keywords": ...,
  "num_days": ...,
  "criteria": ...
}}
(if the user query can not be mapped to the function, return a json with an error message)
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

  def parse(self, input, fid_origin=None):
    prompt = instructions_and_request(parse_instructions, input)
    self.params = call_llm(prompt)
    self.channel = read_channel(self.params)
    self.criteria = read_string(self.params, 'criteria', 'most interesting', 100)
    self.num_days = read_int(self.params, 'num_days', 7, 1, 10)
    self.max_rows = 100
    self.keywords = read_keywords(self.params)
    
  def get_cost(self):
    sql, params = top_casts_sql(self.channel, self.num_days, self.max_rows, self.keywords)
    test = dry_run(sql, params)
    self.cost = test['cost']
    return self.cost

  def execute(self):
    posts = top_casts_results(self.channel, self.num_days, self.max_rows, self.keywords)
    if len(posts) < 10:
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
  action.parse(input)
  print(f"Channel: {action.channel}")
  print(f"Criteria: {action.criteria}")
  print(f"Num days: {action.num_days}") 
  print(f"Keywords: {action.keywords}")
  print(f"Max rows: {action.max_rows}")
  cost = action.get_cost()
  print(f"Cost: {cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts(intro='🗞️ Channel Digest 🗞️')
  print(f"Casts: {action.casts}")
  