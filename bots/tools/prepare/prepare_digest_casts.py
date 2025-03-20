from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.data.casts import get_top_casts, get_more_like_this
from bots.utils.format_cast import concat_casts
from bots.utils.llms import get_max_capactity
from bots.utils.check_links import check_link_data
from bots.utils.word_counts import get_word_counts


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


def prepare_digest_casts(input):
  state = input.state
  llm = input.llm
  params = state.action_params
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
  instructions = state.format(main_instructions_intro_template)
  instructions += main_instructions.replace("ADDITIONAL_NOTES?", focus)
  result = call_llm(llm,prompt,instructions,main_schema)
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
  state.digest_casts_data = data
  # Prepare word cloud data
  top_n = 100
  word_counts = get_word_counts([x['text'] for x in posts], top_n)
  if len(word_counts) > 5:
    state.wordcloud_text = data['summary']
    state.wordcloud_counts = word_counts
  return {
    'digest_casts_data': state.digest_casts_data, 
    'wordcloud_text': state.wordcloud_text, 
    'wordcloud_counts': state.wordcloud_counts
  }


PrepareDigestCasts = Tool(
  name="prepare_digest_casts",
  description="Prepare the summary of the posts and select some interesting ones",
  func=prepare_digest_casts
)
