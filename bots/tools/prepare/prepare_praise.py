from langchain.agents import Tool
from bots.utils.llms2 import call_llm


prompt_template = """
# USER ID
@{{user}}

# USER DISPLAY NAME
{{user_display_name}}

# USER BIO
{{user_bio}}

# USER PFP DESCRIPTION
{{user_pfp_description}}

# USER POSTS
{{casts_user}}
"""


instructions_template = """
You are @{{name}}

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#TASK
Your task is to praise {{user}} in a way that feels deeply personal and impactful.

#INSTRUCTIONS:
The name, bio and posts provided are all from @{{user}}.
Analyze their posts carefully.
Based on the provided information, identify their core personality and what makes them unique.
Praise them in a way that is authentic and specific, not vague.
Be yourself and include what you really like about them.
Keep it short but impactful, a poetic appreciation, a clever compliment, or a deep truth about them.
Break down your praise into 3 short tweets:
First tweet introduces them, what makes them special?
Second tweet highlights a strength or quality, with an example from their posts.
Final tweet concludes with a final compliment and another link to one of their posts.
Keep the tweets very short and concise.
When you reference their posts in the second and third tweet, do not include a link in the tweet text - instead, put the id in the json field "link".
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Output 3 sentences in json format.

#RESPONSE FORMAT:
{
  "tweet1": {"text": "..."},
  "tweet2": {"text": "tweet text without the link", "link": "......"},
  "tweet3": {"text": "tweet text without the link", "link": "......"}
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "tweet1":{"type":"OBJECT", "properties":{"text":{"type":"STRING"}}},
    "tweet2":{"type":"OBJECT", "properties":{"text":{"type":"STRING"}, "link":{"type":"STRING"}}},
    "tweet3":{"type":"OBJECT", "properties":{"text":{"type":"STRING"}, "link":{"type":"STRING"}}}
  }
}


def prepare(input):
  state = input.state
  llm = input.llm
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  if 'tweet1' not in result:
    raise Exception('Could not generate a praise')    
  return {
    'data_user_praise': result
  }


PreparePraise = Tool(
  name="PreparePraise",
  description="Generate a user praise",
  metadata={
    'inputs': ['user', 'user_display_name', 'user_bio', 'user_pfp_description', 'casts_user'],
    'outputs': ['data_user_praise']
  },
  func=prepare
)