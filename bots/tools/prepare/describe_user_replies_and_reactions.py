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


def prepare(input):
  state = input.state
  llm = input.llm
  formatted = state.get('user_replies_and_reactions')
  if formatted is None or formatted == '':
    return {'log': 'No replies and reactions to analyze.'}
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  description = result['description'] if 'description' in result else ''
  keywords = result['keywords'] if 'keywords' in result else ''
  if isinstance(keywords, list):
    keywords = ','.join(keywords)
  return {
    'user_replies_and_reactions_description': description,
    'user_replies_and_reactions_keywords': keywords
  }


DescribeUserRepliesAndReactions = Tool(
  name="DescribeUserRepliesAndReactions",
  description="Describe the replies and reactions of a user.",
  metadata={
    'inputs': ['user', 'user_display_name', 'user_bio', 'user_replies_and_reactions'],
    'outputs': ['user_replies_and_reactions_description', 'user_replies_and_reactions_keywords']
  },
  func=prepare
)
