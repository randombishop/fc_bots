from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.read_params import read_channel, read_int, read_keywords
from bots.data.top_casts import top_casts_sql, top_casts_results
from bots.data.bq import dry_run
from bots.utils.prompts import casts_and_instructions
from bots.models.mistral import mistral
from bots.utils.check_links import check_link_data


instructions = """
GENERAL INSTRUCTIONS:
ABOVE ARE SOCIAL MEDIA POSTS FROM A RANDOM SAMPLE OF USERS.
GENERATE A GLOBAL SUMMARY AND SELECT 3 INTERESTING ONES.

DETAILED INSTRUCTIONS:
  - Write a catch phrase title.
  - Generate 3 sentences to describe what the users are talking about, try to cover as much content as possible in these 3 sentences.
  - Include 3 links to reference relevant post ids and comment them with a keyword and emoji.
  - Output the result in json format.
  - Make sure you don't use " inside json strings. Avoid invalid json.

RESPONSE FORMAT:
{
  "title": "...catch phrase...",
  "sentence1": "...",
  "sentence2": "...",
  "sentence3": "...",
  "link1": {"id": "uuid1", "comment": "keyword [emoji]"},
  "link2": {"id": "uuid2", "comment": "keyword [emoji]"},
  "link3": {"id": "uuid3", "comment": "keyword [emoji]"}
}
"""


class DigestCasts(IAction):

  def __init__(self, params):
    super().__init__(params)
    self.channel = read_channel(params)
    self.num_days = read_int(params, 'days', 1, 1, 10)
    self.max_rows = 100
    self.keywords = read_keywords(params)
    
  def get_cost(self):
    sql, params = top_casts_sql(self.channel, self.num_days, self.max_rows, self.keywords)
    test = dry_run(sql, params)
    if 'error' in test:
      self.error = test['error']
      return 0
    else:
      self.cost = test['cost']
      return self.cost

  def execute(self):
    # Get data
    posts = top_casts_results(self.channel, self.num_days, self.max_rows, self.keywords)
    posts.sort(key=lambda x: x['timestamp'])
    # Run LLM
    prompt = casts_and_instructions(posts, instructions)
    result_string = mistral(prompt)
    try:
      result = json.loads(result_string)
    except:
      print(f"Error parsing json: {result_string}")
      return self.result
    # Make summary
    summary = []
    if 'sentence1' in result and len(result['sentence1']) > 0:
      summary.append(result['sentence1'])
    if 'sentence2' in result and len(result['sentence2']) > 0   :
      summary.append(result['sentence2'])
    if 'sentence3' in result and len(result['sentence3']) > 0:
      summary.append(result['sentence3'])
    try:
      del result['sentence1']
      del result['sentence2']
      del result['sentence3']
    except:
      pass
    result['summary'] = summary
    # Make links
    posts_map = {x['hash']: x for x in posts}
    links = []
    for link_key in ['link1', 'link2', 'link3']:
        if link_key in result:
            link = check_link_data(result[link_key], posts_map)
            if link is not None:
                links.append(link)
            del result[link_key]
    result['links'] = links
    # Done
    self.result = result
    return self.result
  
  def get_casts(self, intro=''):
    casts = []
    cast1 = (intro + '\n\n' + self.result['title'] + '\n\n' + self.result['summary'][0]).strip()
    casts.append({'text': cast1})
    for t in self.result['summary'][1:]:
        casts.append({'text': t})
    for link in self.result['links']:
        casts.append({'text': link['comment'], 'embed': {'fid': link['fid'], 'user_name': link['user_name'], 'hash': link['id']}})
    self.casts = casts
    return self.casts


if __name__ == "__main__":
  channel = sys.argv[1] if len(sys.argv) > 1 else None
  num_days = sys.argv[2] if len(sys.argv) > 2 else None
  keywords = sys.argv[3] if len(sys.argv) > 3 else None
  params = {'channel': channel, 'days': num_days, 'keywords': keywords}
  digest = DigestCasts(params)
  print(f"Num days: {digest.num_days}")
  print(f"Channel: {digest.channel}")
  print(f"Keywords: {digest.keywords}")
  print(f"Max rows: {digest.max_rows}")
  cost = digest.get_cost()
  print(f"Cost: {cost}")
  digest.execute()
  print(f"Result: {digest.result}")
  if digest.result is not None:
    digest.get_casts(intro='🗞️ Channel Digest 🗞️')
    print(f"Casts: {digest.casts}")