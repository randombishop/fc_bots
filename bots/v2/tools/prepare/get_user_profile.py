from langchain.agents import Tool
from bots.v2.call_llm import call_llm
from bots.data.wield import get_user_info_by_name
from bots.data.casts import get_top_casts
from bots.prompts.format_casts import concat_casts


prompt_template = """
# USER ID
@{{user}}

# USER DISPLAY NAME
{{user_display_name}}

# USER BIO
{{user_bio}}

# USER POSTS
{{about_user}}
"""


instructions_template = """
You are @{{name}} bot

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#INSTRUCTIONS:
You are analyzing posts from @{{user}} on the social media platform Farcaster. 
Your goal is to write 2 short sentences to describe their profile in your own words and style.
Analyze their posts carefully to understand their expertise, interests, passions, life style and humor themes.
Extract the topics that are important for them.
Your output will be published in their profile under the rubric "What they cast about."
Your descrition should be positive and respectful.
Your goal is not to summarize the actual content they posted, you must instead capture what they typically cast about.
Avoid judgment or personal opinions and keep your description neutral.
Make sure you don't use " inside json strings. Avoid invalid json.
Output 2 sentences in json format.

#RESPONSE FORMAT:
{
  "sentence1": "..."
  "sentence2": "..."
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "sentence1":{"type":"STRING"},
    "sentence2":{"type":"STRING"}
  }
}


def get_user_profile(input):
  state = input['state']
  llm = input['llm']
  if state.user_casts_description is not None:
    return
  user_name = state.user
  if user_name is None:
    raise Exception(f"Missing user name in context.")
  user_info = get_user_info_by_name(user_name)
  df = get_top_casts(user_name=user_name, max_rows=50)
  posts = df.to_dict('records') if len(df) > 0 else []
  formatted_posts = concat_casts(posts)
  state.user_casts = posts
  for x in posts:
    state.posts_map[x['id']] = x
  state.about_user = formatted_posts
  state.user_display_name = user_info['display_name']
  state.user_bio = user_info['bio']['text'] 
  state.user_followers = user_info['num_followers']
  state.user_following = user_info['num_following']
  if 'pfp' in user_info and user_info['pfp'] is not None and 'url' in user_info['pfp']:
    state.user_pfp_url = user_info['pfp']['url']
  if len(posts)>0:
    prompt = state.format(prompt_template)
    instructions = state.format(instructions_template)
    result = call_llm(llm, prompt, instructions, schema)
    user_casts_description = ''
    if 'sentence1' in result:
      user_casts_description += result['sentence1'] + '\n'
    if 'sentence2' in result:
      user_casts_description += result['sentence2']
    state.user_casts_description = user_casts_description
  return {
    'about_user': state.about_user,
    'user_display_name': state.user_display_name,
    'user_bio': state.user_bio,
    'user_followers': state.user_followers,
    'user_following': state.user_following,
    'user_pfp_url': state.user_pfp_url,
    'user_casts_description': state.user_casts_description
  }
  

GetUserProfile = Tool(
  name="get_user_profile",
  description="Process the user data to generate a profile description",
  func=get_user_profile
)
