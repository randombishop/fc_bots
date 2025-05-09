from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.format_cast import extract_cast, format_casts
from bots.utils.format_state import format_template, format_state


instructions_template = """
You are @{{bot_name}} bot

#YOUR BIO:
{{bio}}

#YOUR LORE:
{{lore}}

#YOUR STYLE:
{{style}}

#GOAL
{{request}}

#TASK:
Your task is to respond to a user on a social media platform based on the provided context and instructions.
Output 1 response post or a thread of up to 3 posts max in json format.
Prefer a response in 1 single post if possible, but you can use 2 or 3 posts if really needed.
For your information, in the farcaster social media platform, posts are called casts.
When you include urls or post ids, always put them between brackets like this [https://...] or [0x......]
When you mention users, always use the @username format, no need to put them between brackets or parentheses or any other special characters.
Avoid mentioning more than 3 users in a single post.
Avoid phrasing your post like previous similar ones or copying from other posts.
Output the result in json format.
Make sure you don't use " inside json strings. 
Avoid invalid json.


#RESPONSE PLAN:
{{response_plan}}

#RESPONSE FORMAT:
{
  "post1": "...",
  "post2": "...",
  "post3": "..."
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "post1":{"type":"STRING"},
    "post2":{"type":"STRING"},
    "post3":{"type":"STRING"}
  }
}


def _compose(state):
  state.composed = True
  prompt = format_state(state, intro=True, variables=True)
  instructions = format_template(instructions_template, {
    'bot_name': state.bot_name,
    'bio': state.get_variable('bio').value,
    'lore': state.get_variable('lore').value,
    'style': state.get_variable('style').value,
    'request': state.request,
    'response_plan': state.plan['response_plan']
  })
  result = call_llm('large', prompt, instructions, schema)
  posts_map = {}
  for v in state.variables.values():
    if v.get_type() == 'Casts':
      casts = v.value.casts
      for c in casts:
        posts_map[c.id] = c
  casts = []
  def add_cast(num):
    if f'post{num}' in result and result[f'post{num}'] is not None and len(result[f'post{num}']) > 0:
      text = result[f'post{num}']
      casts.append(extract_cast(text, posts_map, state.get_variable('style').value))
  add_cast(1)
  add_cast(2)
  add_cast(3)
  state.casts = casts
  return {
    'casts': casts,
    'formatted': format_casts(casts)
  }


compose = Tool(
  name="compose",
  description="Compose one or multiple casts.",
  func=_compose
)
