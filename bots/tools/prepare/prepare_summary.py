from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.format_cast import concat_casts
from bots.utils.check_links import check_link_data
from bots.utils.word_counts import get_word_counts


instructions_template = """
#TASK 
Your task is to generate a global summary of the provided social media posts.
Write a short summary tweet.
Include 3 links to reference relevant post ids and comment them.
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
Don't reference websites and don't include any urls in your summary.
Study the provided data and instructions carefully to generate a summary that is relevant to the instructions intent.

#RESPONSE FORMAT
{
  "tweet": "Catch phrase summarizing the posts",
  "link1": {"id": "......", "comment": "..."},
  "link2": {"id": "......", "comment": "..."},
  "link3": {"id": "......", "comment": "..."}
}
"""

schema = {
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


def prepare(input):
  state = input.state
  llm = input.llm
  # Run LLM
  prompt = state.format_all()
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  data = {}
  # Extract summary
  if 'tweet' not in result or len(result['tweet']) < 10:
    raise Exception('Could not generate a summary')
  data['summary'] = result['tweet']
  # Make links
  posts_map = state.posts_map
  links = []
  for link_key in ['link1', 'link2', 'link3']:
    if link_key in result:
      link = check_link_data(result[link_key], posts_map)
      if link is not None:
        links.append(link)
      del result[link_key]
  data['links'] = links
  summary = data['summary']
  for link in links:
    summary += f"\n{link['comment']}"
  return {
    'data_summary': state.digest_casts_data, 
    'summary': summary
  }


PrepareSummary = Tool(
  name="PrepareSummary",
  description="Prepare the summary of the posts and select some interesting ones",
  metadata={
    'inputs': ['casts_category', 'casts_channel', 'casts_keyword', 'casts_search', 'casts_user', 'casts_text'],
    'require_inputs': 'any',
    'outputs': ['data_summary', 'summary']
  },
  func=prepare
)
