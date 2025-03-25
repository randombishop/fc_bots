from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.data.casts import get_user_replies_and_reactions
from bots.utils.format_cast import format_when, shorten_text


prompt_template = """
# USER ID
@{{user}}

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


def describe_user_replies_and_reactions(input):
  state = input.state
  llm = input.llm
  if state.user_replies_and_reactions_description is not None:
    return {'log': 'User replies and reactions description already set.'}
  formatted = state.user_replies_and_reactions
  if formatted is None or formatted == '':
    return {'log': 'No replies and reactions to analyze.'}
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  description = result['description'] if 'description' in result else ''
  keywords = result['keywords'] if 'keywords' in result else ''
  state.user_replies_and_reactions_description = description
  state.user_replies_and_reactions_keywords = keywords
  return {
    'user_replies_and_reactions_description': state.user_replies_and_reactions_description,
    'user_replies_and_reactions_keywords': state.user_replies_and_reactions_keywords
  }


DescribeUserRepliesAndReactions = Tool(
  name="DescribeUserRepliesAndReactions",
  description="Describe the replies and reactions of a user",
  func=describe_user_replies_and_reactions
)
