from bots.kit_interface.user_reactions_description import UserReactionsDescription
from bots.kit_interface.user_id import UserId
from bots.kit_interface.user_profile import UserProfile
from bots.kit_interface.reactions import Reactions
from bots.kit_interface.bio import Bio
from bots.kit_interface.style import Style
from bots.kit_interface.lore import Lore
from bots.utils.prompts import format_template
from bots.utils.llms2 import call_llm



prompt_template = """
# USER ID
@{{user_name}}

# USER DISPLAY NAME
{{user_display_name}}

# USER BIO
{{user_bio}}

# USER POSTS
{{user_replies_and_reactions}}
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
You are analyzing replies, likes and recasts from @{{user}} on the social media platform Farcaster. 
Your goal is to describe the kind of content and topics they typically engage with.
Analyze their replies, likes and reposts carefully to understand their interests and preferences.
Extract the topics that they find interesting.
Your output will be published in their profile under the rubric "What they react to"
Your descrition should be positive and respectful.
Your goal is not to summarize the actual content they engage with, you must instead capture what they typically like in more general terms and keywords.
Avoid judgment or personal opinions and keep your description neutral.
Output your description in one sentence, plus a list of keywords.
Make sure you don't use " inside json strings. Avoid invalid json.
Output your description and keywords in the following json format. 

#RESPONSE FORMAT:
{
  "description": "..."
  "keywords": "comma separated list of keywords"
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "description":{"type":"STRING"},
    "keywords":{"type":"STRING"}
  }
}


def describe_user_reactions(bot_name: str, bio: Bio, lore: Lore, style: Style, 
                                        user_id: UserId, user_profile: UserProfile, reactions: Reactions) -> UserReactionsDescription:
  prompt = format_template(prompt_template, {
    'user_name': user_id.username,
    'user_display_name': user_profile.display_name,
    'user_bio': user_profile.bio,
    'user_replies_and_reactions': reactions
  })
  instructions = format_template(instructions_template, {
    'name': bot_name,
    'bio': bio,
    'lore': lore,
    'style': style,
    'user': user_id.username
  })
  result = call_llm('medium', prompt, instructions, schema)
  description = result['description'] if 'description' in result else ''
  keywords = result['keywords'] if 'keywords' in result else ''
  return UserReactionsDescription(description, keywords)

