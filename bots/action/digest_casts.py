import uuid
import os
from bots.i_action_step import IActionStep
from bots.utils.read_params import read_channel, read_keyword, read_category, read_string, read_user
from bots.data.casts import get_top_casts, get_more_like_this
from bots.prompts.format_casts import concat_casts
from bots.utils.llms import call_llm, get_max_capactity
from bots.utils.check_links import check_link_data
from bots.utils.word_counts import get_word_counts
from bots.data.channels import get_channel_url
from bots.autoprompt.summary_prompt_in_channel import summary_prompt_in_channel
from bots.autoprompt.summary_prompt_no_channel import summary_prompt_no_channel
from bots.prepare.get_wordcloud import GetWordcloud
from bots.prepare.get_mask import GetMask


parse_instructions_template = """
#CURRENT CHANNEL
{{selected_channel}}

#INSTRUCTIONS
You are @{{name}}, a bot programmed to make summaries of posts (=casts) in a social media platform.
You have access to an API that can generate the summary based on these parameters: category, channel, keyword, search, user.
* category: Can be one of pre-defined categories 'arts', 'business', 'crypto', 'culture', 'money', 'nature', 'politics', 'sports', 'tech_science'.
* channel: Channels always start with '/', for example '/data', if there is no '/' then it's not a channel.
* keyword: Any single keyword, if something can't be mapped to a category and doesn't look like a channel, you can use it as a keyword, but only if it's a single word.
* search: If the summary is not about a category, channel, keyword or user; then formulate a search phrase to search for posts and summarize them.
* user: User names typically start with `@`, if the intent is to summarize posts by a specific user, you can use the user parameter.
Your goal is not to continue the conversation, you must only extract the parameters to call the API.
You can use the conversation to guess the parameters, but focus on the request.
Your goal is to extract the parameters from the request.

#RESPONSE FORMAT
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

main_instructions_intro_template = """
You are @{{name}}, a bot programmed to make summaries of posts (=casts) in a social media platform.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#CURRENT CHANNEL
{{selected_channel}}
"""

main_instructions = """
#GENERAL INSTRUCTIONS
YOUR TASK IS TO GENERATE A GLOBAL SUMMARY AND SELECT 3 INTERESTING ONES FROM THE PROVIDED SOCIAL MEDIA POSTS.

#DETAILED INSTRUCTIONS
Write a short summary tweet.
Include 3 links to reference relevant post ids and comment them.
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
Focus on posts that are genuine, interesting, funny, or informative.
Don't reference websites and don't include any urls in your summary.
ADDITIONAL_NOTES?

#RESPONSE FORMAT
{
  "tweet": "Catch phrase summarizing ",
  "link1": {"id": "......", "comment": "keyword [emoji]"},
  "link2": {"id": "......", "comment": "keyword [emoji]"},
  "link3": {"id": "......", "comment": "keyword [emoji]"}
}
"""

main_schema = {
  "type":"OBJECT",
  "properties":{
    "title":{"type":"STRING"},
    "sentence1":{"type":"STRING"},
    "sentence2":{"type":"STRING"},
    "sentence3":{"type":"STRING"},
    "link1":{
       "type":"OBJECT", 
       "properties":{
         "id":{"type":"STRING"},
         "comment":{"type":"STRING"}
       }
    },
    "link2":{
       "type":"OBJECT", 
       "properties":{
         "id":{"type":"STRING"},
         "comment":{"type":"STRING"}
       }
    },
    "link3":{
       "type":"OBJECT", 
       "properties":{
         "id":{"type":"STRING"},
         "comment":{"type":"STRING"}
       }
    }  
  }
}


class DigestCasts(IActionStep):
    
  def get_cost(self):
    return 20

  def auto_prompt(self):
    channel_url = get_channel_url(self.state.selected_channel)
    prompt, params, log = None, None, ''
    if channel_url is None:
      prompt, params, log = summary_prompt_no_channel(self.state)
    else:
      prompt, params, log = summary_prompt_in_channel(self.state)
    self.state.action_params = params
    self.state.request = prompt
    self.state.conversation = self.state.request
    self.state.log += log+'\n'
  
  def parse(self):
    parse_prompt = self.state.format_conversation()
    parse_instructions = self.state.format(parse_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_schema)
    parsed = {}
    parsed['channel'] = read_channel(params)
    parsed['keyword'] = read_keyword(params)
    parsed['category'] = read_category(params)
    parsed['search'] = read_string(params, key='search', default=None, max_length=500)
    _, user_name = read_user(params, fid_origin=self.state.fid_origin, default_to_origin=False)
    parsed['user_name'] = user_name
    self.state.action_params = parsed
      
  def execute(self):
    params = self.state.action_params
    if params is None:
      raise Exception('Summary params were not parsed')
    params['max_rows'] = get_max_capactity()
    # Get data
    posts = []
    if 'search' in params and params['search'] is not None:
      posts = get_more_like_this(params['search'], limit=params['max_rows'])
    else:
      posts = get_top_casts(channel=params['channel'] if 'channel' in params else None,
                            keyword=params['keyword'] if 'keyword' in params else None,
                            category=params['category'] if 'category' in params else None,
                            user_name=params['user_name'] if 'user_name' in params else None,
                            max_rows=params['max_rows'])
    posts = posts.to_dict('records')
    posts.sort(key=lambda x: x['timestamp'])
    if len(posts) < 5:
      raise Exception(f"""Not enough posts to generate a digest: channel={params['channel']}, 
                      keyword={params['keyword']}, category={params['category']}, max_rows={params['max_rows']}, posts={len(posts)}""")
    # Focus directive
    focus = ''
    if 'keyword' in params and params['keyword'] is not None:
      focus = ("Focus on the following subject: " + params['keyword'] + "\n")
    if 'category' in params and params['category'] is not None:
      focus =  ("Focus on the following category: " + params['category'][2:] + "\n")
    if 'user_name' in params and params['user_name'] is not None:
      focus =  ("The posts are all from user @" + params['user_name'] + ", be respectful in your summary and only mention them in positive terms.\n")
    # Run LLM
    prompt = concat_casts(posts)
    instructions = self.state.format(main_instructions_intro_template)
    instructions += main_instructions.replace("ADDITIONAL_NOTES?", focus)
    result = call_llm(prompt,instructions,main_schema)
    data = {}
    # Extract summary
    if 'tweet' not in result or len(result['tweet']) < 10:
      raise Exception('Could not generate a summary')
    data['summary'] = result['tweet']
    # Make links
    posts_map = {x['id']: x for x in posts}
    links = []
    for link_key in ['link1', 'link2', 'link3']:
      if link_key in result:
        link = check_link_data(result[link_key], posts_map)
        if link is not None:
          links.append(link)
        del result[link_key]
    data['links'] = links
    # Make word cloud
    top_n = 100
    word_counts = get_word_counts([x['text'] for x in posts], top_n)
    if len(word_counts) > 5:
      self.state.wordcloud_text = data['summary']
      self.state.wordcloud_counts = word_counts
      GetMask(self.state).prepare()
      GetWordcloud(self.state).prepare()      
      data['wordcloud'] = self.state.wordcloud_url
    casts = []
    cast1 = {'text': data['summary']}
    if 'wordcloud' in data:
      cast1['embeds'] = [data['wordcloud']]
      cast1['embeds_description'] = 'Wordcloud of words used in the posts'
    casts.append(cast1)
    for link in data['links']:
      casts.append({
        'text': link['comment'], 
        'embeds': [{'fid': link['fid'], 'user_name': link['user_name'], 'hash': link['hash']}],
        'embeds_description': link['text']
      })
    self.state.casts = casts


