from langchain.agents import Tool
from bots.utils.llms2 import call_llm


prompt_template = """
# USER ID
@{{user}}

# USER DISPLAY NAME
{{user_display_name}}

# USER BIO
{{user_bio}}

# USER POSTS
{{about_user_origin}}
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
Your goal is to write 3 short bullet points to describe their profile in your own words and style.
Analyze their posts carefully to understand their expertise, interests, passions, life style and humor themes.
Extract the topics that are important for them.
Your output will be published in their profile under the rubric "What they cast about."
Your descrition should be positive and respectful.
Your goal is not to summarize the actual content they posted, you must instead capture what they typically cast about.
Avoid judgment or personal opinions and keep your description neutral.
Avoid vague statements like "they positively engage with the community" or "they are passionate about connecting with others".
Avoid generic qualities like ""they have a playful and friendly tone" that most users feature in a social media platform.
Emphasize unique and specific features that are not often found in social media profiles.
Make sure you don't use " inside json strings. Avoid invalid json.
Output 3 short sentences in json format.

#RESPONSE FORMAT:
{
  "sentence1": "...",
  "sentence2": "...",
  "sentence3": "..."
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "sentence1":{"type":"STRING"},
    "sentence2":{"type":"STRING"},
    "sentence3":{"type":"STRING"}
  }
}


def describe_user_casts(input):
  state = input.state
  llm = input.llm
  if state.user_casts_description is not None:
    return {'log': 'Casts description already set.'}
  posts = state.user_casts
  if len(posts) == 0:
    return {'log': 'No posts to analyze.'}
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  user_casts_description = ''
  if 'sentence1' in result:
    user_casts_description += result['sentence1'] + '\n'
  if 'sentence2' in result:
    user_casts_description += result['sentence2'] + '\n'
  if 'sentence3' in result:
    user_casts_description += result['sentence3']
  state.user_casts_description = user_casts_description
  return {
    'user_casts_description': state.user_casts_description
  }
  

DescribeUserCasts = Tool(
  name="DescribeUserCasts",
  description="Describe the user's casts",
  metadata={
    'inputs': 'Requires user_casts to be fetched first using get_profile tool.',
    'outputs': 'user_casts_description'
  },
  func=describe_user_casts
)
