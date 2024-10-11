from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.read_params import read_channel, read_int, read_keywords, read_category
from bots.data.top_casts import top_casts_sql, top_casts_results
from bots.data.bq import dry_run
from bots.utils.prompts import instructions_and_request, casts_and_instructions
from bots.utils.llms import call_llm
from bots.utils.check_links import check_link_data
from bots.utils.check_casts import check_casts

parse_instructions = """
INSTRUCTIONS:
Find one or more of the following parameters in the user input: category, channel, keywords and number of days. 
Your goal is not to answer the user query, you only need to extract the parameters.
The query doesn't need to match a specific format, your job is to guess the parameters that the user is asking for.

PARAMETERS
* channel, optional, defaults to null.
* category, optional, one of pre-defined categories, defaults to null. Allowed categories are: 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* keywords, optional, comma separated list of keywords, defaults to null.
* num_days is an optional parameter and defaults to 1  

RESPONSE FORMAT:
{
  "category": ...,
  "channel": ...,
  "keywords": ...,
  "num_days": ...,
}
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
- Don't reference websites and don't include any urls in your summary.
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
    
  def set_input(self, input):
    prompt = instructions_and_request(parse_instructions, input)
    params = call_llm(prompt)
    self.set_params(params)

  def set_params(self, params):
    self.channel = read_channel(params)
    self.keywords = read_keywords(params)
    self.category = read_category(params)
    self.num_days = read_int(params, 'num_days', 7, 1, 10)
    self.max_rows = 100
    if debug:
      print("DigestCasts.set_params():")
      print(f"  channel: {self.channel}")
      print(f"  num_days: {self.num_days}")
      print(f"  max_rows: {self.max_rows}")
      print(f"  keywords: {self.keywords}")
      print(f"  category: {self.category}")

  def get_cost(self):
    sql, params = top_casts_sql(channel=self.channel, num_days=self.num_days, 
                                max_rows=self.max_rows, keywords=self.keywords, 
                                category=self.category, informative=True)
    test = dry_run(sql, params)
    self.cost = test['cost']
    if debug:
      print("DigestCasts.get_cost():")
      print(f"  sql: {sql}")
      print(f"  params: {params}")
      print(f"  cost: {self.cost}")
    return self.cost

  def get_data(self):
    # Get data
    posts = top_casts_results(channel=self.channel, num_days=self.num_days, 
                              max_rows=self.max_rows, keywords=self.keywords, 
                              category=self.category, informative=True)
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
  action = DigestCasts()
  action.set_input(input)
  cost = action.get_cost()
  print(f"Cost: {cost}")
  action.get_data()
  print(f"Data: {action.data}")
  action.get_casts(intro='🗞️ Channel Digest 🗞️')
  print(f"Casts: {action.casts}")
