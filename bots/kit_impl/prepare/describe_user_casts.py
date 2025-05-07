from bots.kit_interface.user_casts_description import UserCastsDescription
from bots.kit_interface.user_id import UserId
from bots.kit_interface.user_profile import UserProfile
from bots.kit_interface.casts import Casts
from bots.kit_interface.bio import Bio
from bots.kit_interface.style import Style
from bots.kit_interface.lore import Lore
from bots.utils.format_state import format_template
from bots.utils.llms2 import call_llm


prompt_template = """
# USER NAME
@{{user_name}}

# USER DISPLAY NAME
{{user_display_name}}

# USER BIO
{{user_bio}}

# USER POSTS
{{casts_user}}
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


def describe_user_casts(bot_name: str, bio: Bio, lore: Lore, style: Style, user_id: UserId, user_profile: UserProfile, casts: Casts) -> UserCastsDescription:
  prompt = format_template(prompt_template, {
    'user_name': user_id.username,
    'user_display_name': user_profile.display_name,
    'user_bio': user_profile.bio,
    'casts_user': str(casts)
  })
  instructions = format_template(instructions_template, {
    'name': bot_name,
    'bio': bio,
    'lore': lore,
    'style': style,
    'user': user_id.username
  })
  result = call_llm('medium', prompt, instructions, schema)
  user_casts_description = ''
  if 'sentence1' in result:
    user_casts_description += result['sentence1'] + '\n'
  if 'sentence2' in result:
    user_casts_description += result['sentence2'] + '\n'
  if 'sentence3' in result:
    user_casts_description += result['sentence3']
  return UserCastsDescription(user_casts_description)
  
