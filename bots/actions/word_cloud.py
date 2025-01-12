from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
from bots.iaction import IAction
from bots.data.casts import get_top_casts, get_more_like_this
from bots.utils.llms import call_llm
from bots.utils.read_params import read_channel, read_user, read_string, read_category, read_keyword
from bots.utils.images import make_wordcloud
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts
from bots.utils.word_counts import get_word_counts


parse_instructions = """
INSTRUCTIONS:
You are @dsart, a bot programmed to make a wordcloud based on posts (=casts) in a social media platform.
You have access to an API that can generate the wordcloud based on these parameters: category, channel, keyword, search, user.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* search: If the wordcloud is not about a category, channel, keyword or user; then formulate a search phrase to search for posts.
* user: User names typically start with `@`, if the intent is to make the wordcloud for a specific user, you can use the user parameter.
Your goal is not to continue the conversation, you must only extract the parameters to call the API.

RESPONSE FORMAT:
{
  "category": "...",
  "channel": "...",
  "keyword": "...",
  "search": "...",
  "user": "..."
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "category":{"type":"STRING"},
    "channel":{"type":"STRING"},
    "keyword":{"type":"STRING"},
    "search":{"type":"STRING"},
    "user":{"type":"STRING"}
  }
}



class WordCloud(IAction):
  
  
  def set_input(self, input):
    params = call_llm(input, parse_instructions, parse_schema)
    self.input = input
    self.set_params(params)

  def set_params(self, params):
    self.channel = read_channel(params)
    self.keyword = read_keyword(params)
    self.category = read_category(params)
    self.search = read_string(params, key='search', default=None, max_length=500)
    self.fid, self.user_name = read_user(params, fid_origin=self.fid_origin, default_to_origin=False)
    self.max_rows = 250

  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    top_n = 50
    posts = []
    if self.search is not None:
      posts = get_more_like_this(self.search, limit=self.max_rows)
    else:
      posts = get_top_casts(channel=self.channel,
                            keyword=self.keyword,
                            category=self.category,
                            user_name=self.user_name,
                            max_rows=self.max_rows)
    if posts is None or len(posts) == 0:
      raise Exception(f"Not enough activity to buid a word cloud.")
    posts = posts['text'].tolist()
    word_counts = get_word_counts(posts, top_n)
    if len(word_counts) == 5:
      raise Exception(f"Not enough activity to buid a word cloud.")
    self.data = word_counts
    
  def get_casts(self, intro=''):
    filename = str(uuid.uuid4())+'.png'
    make_wordcloud(self.data, filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    cast = {
      'text': "", 
      'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"]
    }
    if self.fid is not None and self.user_name is not None:
      cast['mentions'] = [self.fid]
      cast['mentions_pos'] = [0]
      cast['mentions_ats'] = [f"@{self.user_name}"]
    casts =  [cast]
    check_casts(casts)
    self.casts = casts
    return self.casts
