from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.read_params import read_channel, read_int, read_keywords, read_string
from bots.data.top_casts import top_casts_sql, top_casts_results
from bots.data.bq import dry_run
from bots.utils.prompts import casts_and_instructions
from bots.models.mistral import mistral
from bots.utils.check_links import check_link_data


instructions = """
INSTRUCTIONS:
  - Select the best post from this list above using this criteria: {}
  - Comment about the post with a keyword and emoji.
  - Output the result in json format.
  - Make sure you don't use " inside json strings. Avoid invalid json.

RESPONSE FORMAT:
{{
  "id": "selected post uuid",
  "text": "original text of the post",
  "comment": "comment on the post with a keyword and emoji",
}}
"""


class PickCast(IAction):

  def __init__(self, params):
    super().__init__(params)
    self.channel = read_channel(params)
    self.criteria = read_string(params, 'criteria', 'most interesting', 100)
    self.num_days = read_int(params, 'num_days', 1, 1, 10)
    self.max_rows = 100
    self.keywords = read_keywords(params)
    
  def get_cost(self):
    sql, params = top_casts_sql(self.channel, self.num_days, self.max_rows, self.keywords)
    test = dry_run(sql, params)
    self.cost = test['cost']
    return self.cost

  def execute(self):
    posts = top_casts_results(self.channel, self.num_days, self.max_rows, self.keywords)
    if len(posts) < 10:
      raise Exception(f"Not enough posts to pick a winner ({len(posts)} posts)")
    prompt = casts_and_instructions(posts, instructions.format(self.criteria))
    result_string = mistral(prompt)
    result = json.loads(result_string)
    posts_map = {x['hash']: x for x in posts}
    result = check_link_data(result, posts_map)
    self.result = result
    return result
    
  def get_casts(self, intro=''):
    casts = []
    cast = {
      'text': self.result['comment'],
      'embed': {'fid': self.result['fid'], 'user_name': self.result['user_name'], 'hash': self.result['id']}
    }
    casts.append(cast)
    self.casts = casts
    return self.casts


if __name__ == "__main__":
  channel = sys.argv[1] if len(sys.argv) > 1 else None
  criteria = sys.argv[2] if len(sys.argv) > 2 else None
  num_days = sys.argv[3] if len(sys.argv) > 3 else None
  keywords = sys.argv[4] if len(sys.argv) > 4 else None
  params = {'channel': channel, 'criteria': criteria, 'num_days': num_days, 'keywords': keywords}
  digest = PickCast(params)
  print(f"Channel: {digest.channel}")
  print(f"Criteria: {digest.criteria}")
  print(f"Num days: {digest.num_days}") 
  print(f"Keywords: {digest.keywords}")
  print(f"Max rows: {digest.max_rows}")
  cost = digest.get_cost()
  print(f"Cost: {cost}")
  digest.execute()
  print(f"Result: {digest.result}")
  digest.get_casts(intro='🗞️ Channel Digest 🗞️')
  print(f"Casts: {digest.casts}")
  