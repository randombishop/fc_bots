from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.format_cast import concat_casts
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
{{channel}}
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


def prepare_summary(input):
  state = input.state
  llm = input.llm
  posts = state.casts_for_params
  if posts is None:
    raise Exception("No posts to summarize")
  if len(posts) < 5:
    raise Exception("Not enough posts to summarize")
  # Focus directive
  focus = ''
  if state.keyword is not None:
    focus = ("Focus on the following subject: " + state.keyword + "\n")
  if state.category is not None:
    focus =  ("Focus on the following category: " + state.category[2:] + "\n")
  if state.user is not None:
    focus =  ("The posts are all from user @" + state.user + ", be respectful in your summary and only mention them in positive terms.\n")
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


PrepareSummary = Tool(
  name="PrepareSummary",
  description="Prepare the summary of the posts and select some interesting ones",
  metadata={
    'inputs': 'Requires casts_for_params to be fetched first using GetCastsForParams tool.',
    'outputs': 'digest_casts_data, wordcloud_text, wordcloud_counts'
  },
  func=prepare_summary
)
