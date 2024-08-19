import json
from bots.iaction import IAction
from bots.data.cast_sample import get_casts_with_top_engagement
from bots.models.mistral import call_model


INSTRUCTIONS = """
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


def make_prompt(posts):
  prompt = 'POSTS:\n'
  for post in posts:
    prompt += "\n"
    prompt += "<"+post['hash']+">\n"
    prompt += post['text']
    prompt += "\n</"+post['hash']+">\n"
  prompt += "\n"
  prompt += '\n\n'
  prompt += INSTRUCTIONS
  return prompt


class Digest(IAction):

  def __init__(self, params):
    super().__init__(params)
    # channel
    self.channel = None
    if ('channel' in params) and (params['channel'] is not None) and (params['channel'] != 'null') and (len(params['channel']) > 0):
      self.channel = params['channel']
    # num_days
    self.num_days = 1
    if 'days' in params:
      self.num_days = int(params['days'])
      self.num_days = min(self.num_days, 10)
    # max_rows
    max_rows = 50
    # keywords
    self.keywords = []
    if 'keywords' in params and len(params['keywords']) > 0:
      keywords_string = params['keywords']
      keywords_string = keywords_string.replace(' ', ',')
      keywords_string = keywords_string.replace('\n', ',')
      keywords_string = keywords_string.lower()
      self.keywords = keywords_string.split(',')
      self.keywords = [keyword.strip() for keyword in self.keywords]
      self.keywords = [
        keyword for keyword in self.keywords if len(keyword) > 3]

  def get_cost(self):
    return self.params['num_days'] * 10

  def execute(self):
    posts = get_casts_with_top_engagement(
      self.channel, self.num_days, self.max_rows, self.keywords)
    posts.sort(key=lambda x: x['timestamp'])
    prompt = make_prompt(posts)
    result_string = call_model(prompt)
    try:
      result = json.loads(result_string)
    except:
      print(f"Error parsing json: {result_string}")
      return None

  def get_casts(self):
    return ["cast1", "cast2"]  # Placeholder casts
