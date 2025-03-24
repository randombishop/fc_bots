from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.format_cast import concat_casts
from bots.data.casts import get_top_casts, get_more_like_this
from bots.utils.check_links import check_link_data


task_instructions_intro_template = """
You are @{{name}}, a bot programmed to pick the best post (=cast) in a social media platform.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}
"""

task_instructions = """
INSTRUCTIONS:
Select the best post from this list above using this criteria: ?
Comment about the post with a keyword and emoji.
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Ignore posts that look like ads, promotions, have links to minting NFTs or any other type of commercial activity.
Focus on posts that are genuine, interesting, funny, or informative.

RESPONSE FORMAT:
{
  "id": "selected post id",
  "comment": "comment on the post with a keyword and emoji",
}
"""

task_schema = {
  "type":"OBJECT",
  "properties":{
    "id":{"type":"STRING"}, 
    "comment":{"type":"STRING"}
  }
}


def compose_pick(input):
  state = input.state
  llm = input.llm
  posts = state.casts_for_params
  if len(posts) < 5:
    raise Exception(f"Not enough posts to pick a winner ({len(posts)} posts)")
  prompt = concat_casts(posts)
  instructions = state.format(task_instructions_intro_template)
  instructions += task_instructions.replace('?', state.criteria)
  result = call_llm(llm, prompt, instructions, task_schema)
  posts_map = {x['id']: x for x in posts}
  data = check_link_data(result, posts_map)
  cast = {
    'text': data['comment'],
    'embeds': [{'fid': data['fid'], 'user_name': data['user_name'], 'hash': data['hash']}],
    'embeds_description': data['text'],
    'embeds_warpcast': f"https://warpcast.com/{data['user_name']}/{data['hash'][:10]}"
  }
  casts = [cast]
  state.casts = casts
  return {
    'casts': state.casts
  }


ComposePick = Tool(
  name="ComposePick",
  description="Pick a post and cast a link to it",
  func=compose_pick,
)
