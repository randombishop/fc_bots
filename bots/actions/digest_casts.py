import json
import sys
from bots.iaction import IAction
from bots.data.channels import get_channels
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


class DigestCasts(IAction):

  def __init__(self, params):
    super().__init__(params)
    # channel
    self.channel = None
    if ('channel' in params) and (params['channel'] is not None) and (params['channel'] != 'null') and (len(params['channel']) > 0):
      channels_by_id, channels_by_name = get_channels()
      channel = params['channel']
      if channel is not None and channel != 'null' and len(channel) > 0:
        channel_lower_case = channel.lower()
        if channel_lower_case in channels_by_id:
            channel = channels_by_id[channel_lower_case]
        elif channel_lower_case in channels_by_name:
            channel = channels_by_name[channel_lower_case]
      self.channel = channel
    # num_days
    self.num_days = 1
    if 'days' in params:
      self.num_days = int(params['days'])
      self.num_days = min(self.num_days, 10)
    # max_rows
    self.max_rows = 50
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
      self.result = json.loads(result_string)
    except:
      print(f"Error parsing json: {result_string}")
      self.result = None
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
  channel = None
  num_days = 1
  keywords = None
  if len(sys.argv) > 2:
    channel = sys.argv[2]
  if len(sys.argv) > 3:
    num_days = int(sys.argv[3])
    num_days = min(num_days, 10)
  if len(sys.argv) > 4:
    keywords = sys.argv[3]
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
  digest.get_casts(intro='🗞️ Channel Digest 🗞️')
  print(f"Casts: {digest.casts}")