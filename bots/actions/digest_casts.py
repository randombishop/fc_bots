from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.read_params import read_channel, read_int, read_keywords
from bots.data.top_casts import top_casts_sql, top_casts_results
from bots.data.bq import dry_run
from bots.utils.prompts import instructions_and_request, casts_and_instructions
from bots.utils.llms import call_llm
from bots.utils.check_links import check_link_data
from bots.utils.check_casts import check_casts

parse_instructions = """
INSTRUCTIONS:
Parse the parameters from the user query to make a digest of posts in a channel, from one of pre-defined categories, or using keyword search. 
Your goal is not to answer the user query, you only need to extract the parameters.

PARAMETERS
* channel, optional,defaults to null.
* category, optional, one of pre-defined categories, defaults to null. Allowed categories are: 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* keywords, optional, comma separated list of keywords, defaults to null.
* num_days is an optional parameter and defaults to 1  

RESPONSE FORMAT:
{{
  "category": ...,
  "channel": ...,
  "keywords": ...,
  "num_days": ...,
}}
(if the user query can not be mapped to the function, return a json with an error message)
"""

instructions1 = """
GENERAL INSTRUCTIONS:
ABOVE ARE SOCIAL MEDIA POSTS FROM A RANDOM SAMPLE OF USERS.
GENERATE A GLOBAL SUMMARY AND SELECT 3 INTERESTING ONES.

DETAILED INSTRUCTIONS:
- Write a catch phrase title.
- Generate 3 sentences to describe what the users are talking about, try to cover as much content as possible in these 3 sentences.
- Include 3 links to reference relevant post ids and comment them with a keyword and emoji.
- Output the result in json format.
- Make sure you don't use " inside json strings. Avoid invalid json.
- Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
- Focus on posts that are genuine, interesting, funny, or informative.
"""

instructions2 = """
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


debug = True

class DigestCasts(IAction):
    
  def parse(self, input, fid_origin=None):
    prompt = instructions_and_request(parse_instructions, input)
    self.params = call_llm(prompt)
    self.channel = read_channel(self.params)
    self.keywords = read_keywords(self.params)
    self.category = None
    self.num_days = read_int(self.params, 'num_days', 7, 1, 10)
    self.max_rows = 100
    if debug:
      print("DigestCasts.init():")
      print(f"  channel: {self.channel}")
      print(f"  num_days: {self.num_days}")
      print(f"  max_rows: {self.max_rows}")
      print(f"  keywords: {self.keywords}")
      print(f"  category: {self.category}")
       
  def get_cost(self):
    sql, params = top_casts_sql(self.channel, self.num_days, self.max_rows, self.keywords)
    test = dry_run(sql, params)
    self.cost = test['cost']
    if debug:
      print("DigestCasts.get_cost():")
      print(f"  sql: {sql}")
      print(f"  params: {params}")
      print(f"  cost: {self.cost}")
    return self.cost

  def execute(self):
    # Get data
    posts = top_casts_results(self.channel, self.num_days, self.max_rows, self.keywords)
    posts.sort(key=lambda x: x['timestamp'])
    if len(posts) < 10:
      raise Exception(f"Not enough posts to generate a digest: {len(posts)}")
    # Run LLM
    instructions = instructions1
    if self.keywords is not None and len(self.keywords) > 0:
      instructions += ("- Focus on the following subject: " + " ".join(self.keywords) + "\n")
    instructions += "\n\n"
    instructions += instructions2
    if debug:
      print(instructions)
    prompt = casts_and_instructions(posts, instructions)
    result = call_llm(prompt)
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
    self.data = result
    return self.data
  
  def get_casts(self, intro=''):
    casts = []
    cast1 = (intro + '\n\n' + self.data['title'] + '\n\n' + self.data['summary'][0]).strip()
    casts.append({'text': cast1})
    for t in self.data['summary'][1:]:
        casts.append({'text': t})
    for link in self.data['links']:
        casts.append({'text': link['comment'], 'embeds': [{'fid': link['fid'], 'user_name': link['user_name'], 'hash': link['id']}]})
    check_casts(casts)
    self.casts = casts
    return self.casts


if __name__ == "__main__":
  input = sys.argv[1] 
  action = DigestCasts(input)
  action.parse()
  print(f"Num days: {action.num_days}")
  print(f"Channel: {action.channel}")
  print(f"Keywords: {action.keywords}")
  print(f"Max rows: {action.max_rows}")
  cost = action.get_cost()
  print(f"Cost: {cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts(intro='🗞️ Channel Digest 🗞️')
  print(f"Casts: {action.casts}")
