from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.check_links import check_link_data


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
{{about_user}}
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


def compose_praise(input):
  state = input.state
  llm = input.llm
  fid = state.user_fid
  user_name = state.user
  if fid is None or user_name is None:
    raise Exception(f"Missing fid/user_name.")
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template)
  result1 = call_llm(llm, prompt, instructions, schema)
  if 'tweet1' not in result1:
    raise Exception('Could not generate a praise')    
  embeds = [state.user_avatar] if state.user_avatar is not None else []
  embeds_description = 'Avatar Img' if state.user_avatar is not None else None
  casts = []
  cast1 = {
    'text': ' '+result1['tweet1']['text'],
    'embeds': embeds,
    'embeds_description': embeds_description,
    'mentions': [fid],
    'mentions_pos': [0],
    'mentions_ats': [f"@{user_name}"]
  }
  casts.append(cast1)
  used_links = []
  def add_cast(key):
    if key in result1 and 'text' in result1[key]:
      c = {'text': result1[key]['text']}
      if 'link' in result1[key]:
        link_id = result1[key]['link']
        if link_id not in used_links:
          used_links.append(link_id)
          l = check_link_data({'id':link_id}, state.posts_map)
          if l is not None:
            c['embeds'] = [{'fid': l['fid'], 'user_name': l['user_name'], 'hash': l['hash']}]
            c['embeds_description'] = l['text']
      casts.append(c)
  add_cast('tweet2')
  add_cast('tweet3')
  state.casts = casts
  log = '<Praise>\n'
  log += 'fid: ' + str(fid) + '\n'
  log += 'user: ' + str(user_name) + '\n'
  log += '</Praise>\n'
  return {
    'casts': state.casts,
    'log': log
  }


ComposePraise = Tool(
  name="ComposePraise",
  description="Cast a user praise",
  func=compose_praise
)