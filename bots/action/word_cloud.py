import uuid
import os
from bots.i_action_step import IActionStep
from bots.data.casts import get_top_casts, get_more_like_this
from bots.utils.llms import call_llm
from bots.utils.read_params import read_channel, read_user, read_string, read_category, read_keyword
from bots.utils.images import make_wordcloud
from bots.utils.gcs import upload_to_gcs
from bots.utils.word_counts import get_word_counts


parse_instructions_template = """
INSTRUCTIONS:
You are @{{name}}, a bot programmed to make a wordcloud based on posts (=casts) in a social media platform.
You have access to an API that can generate the wordcloud based on these parameters: category, channel, keyword, search, user.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* search: If the wordcloud is not about a category, channel, keyword or user; then formulate a search phrase to search for posts.
* user: User names typically start with `@`, if the intent is to make the wordcloud for a specific user, you can use the user parameter.
Your goal is not to continue the conversation, you must only extract the parameters to call the API.
You can use the conversation to guess the parameters, but focus on the request.
Your goal is to extract the parameters from the request.

#CURRENT CHANNEL
{{channel}}

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



class WordCloud(IActionStep):
  
  def get_cost(self):
    return 20

  def parse(self):
    parse_prompt = self.state.format_conversation()
    parse_instructions = self.state.format(parse_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_schema)
    parsed = {}
    parsed['channel'] = read_channel(params)
    parsed['keyword'] = read_keyword(params)
    parsed['category'] = read_category(params)
    parsed['search'] = read_string(params, key='search', default=None, max_length=500)
    fid, user_name = read_user(params, fid_origin=self.state.fid_origin, default_to_origin=False)
    parsed['fid'] = fid
    parsed['user_name'] = user_name
    parsed['max_rows'] = 250
    self.state.action_params = parsed
    self.state.user = user_name

  def execute(self):
    top_n = 50
    posts = []
    if self.state.action_params['search'] is not None:
      posts = get_more_like_this(self.state.action_params['search'], limit=self.state.action_params['max_rows'])
    else:
      posts = get_top_casts(channel=self.state.action_params['channel'],
                            keyword=self.state.action_params['keyword'],
                            category=self.state.action_params['category'],
                            user_name=self.state.action_params['user_name'],
                            max_rows=self.state.action_params['max_rows'])
    if posts is None or len(posts) == 0:
      raise Exception(f"Not enough activity to buid a word cloud.")
    posts = posts['text'].tolist()
    word_counts = get_word_counts(posts, top_n)
    if len(word_counts) == 5:
      raise Exception(f"Not enough activity to buid a word cloud.")
    filename = str(uuid.uuid4())+'.png'
    make_wordcloud(word_counts, filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    cast = {
      'text': "", 
      'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"],
      'embeds_description': 'Wordcloud Image'
    }
    if self.state.action_params['fid'] is not None and self.state.action_params['user_name'] is not None:
      cast['mentions'] = [self.state.action_params['fid']]
      cast['mentions_pos'] = [0]
      cast['mentions_ats'] = [f"@{self.state.action_params['user_name']}"]
    casts =  [cast]
    self.state.casts = casts
