from bots.i_prepare_step import IPrepareStep
from bots.data.wield import get_user_info_by_name
from bots.data.casts import get_top_casts
from bots.prompts.format_casts import concat_casts
from bots.utils.llms import call_llm


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


class GetUserProfile(IPrepareStep):
    
  def prepare(self):
    if self.state.user_casts_description is not None:
      return
    user_name = self.state.user
    if user_name is None:
      raise Exception(f"Missing user name in context.")
    user_info = get_user_info_by_name(user_name)
    df = get_top_casts(user_name=user_name, max_rows=50)
    posts = df.to_dict('records') if len(df) > 0 else []
    formatted_posts = concat_casts(posts)
    self.state.user_casts = posts
    for x in posts:
      self.state.posts_map[x['id']] = x
    self.state.about_user = formatted_posts
    self.state.user_display_name = user_info['display_name']
    self.state.user_bio = user_info['bio']['text'] 
    if 'pfp' in user_info and user_info['pfp'] is not None and 'url' in user_info['pfp']:
      self.state.user_pfp_url = user_info['pfp']['url']
    if len(posts)>0:
      prompt = self.state.format(prompt_template)
      instructions = self.state.format(instructions_template)
      result = call_llm(prompt, instructions, schema)
      user_casts_description = ''
      if 'sentence1' in result:
        user_casts_description += result['sentence1'] + '\n'
      if 'sentence2' in result:
        user_casts_description += result['sentence2']
      self.state.user_casts_description = user_casts_description
    log = '<GetUserProfile>\n'
    log += f"display_name: {self.state.user_display_name}\n"
    log += f"bio: {self.state.user_bio}\n"
    log += f"pfp_url: {self.state.user_pfp_url}\n"
    log += f"casts ({len(posts)}): {self.state.user_casts_description}\n"
    log += '</GetUserProfile>\n'
    self.state.log += log
  