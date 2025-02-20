from bots.i_action_step import IActionStep
from bots.utils.llms import call_llm
from bots.utils.read_params import read_user
from bots.utils.check_links import check_link_data
from bots.data.bot_history import get_random_user_to_praise, get_random_user_to_praise_in_channel
from bots.data.users import get_fid
from bots.data.channels import get_channel_url
from bots.prepare.get_user_profile import GetUserProfile
from bots.prepare.get_pfp_description import GetPfpDescrition
from bots.prepare.new_avatar import NewAvatar


parse_user_instructions_template = """
#INSTRUCTIONS:
You are @{{name}}, a bot programmed to praise a user.
Based on the provided conversation, who should we praise?
Your goal is not to continue the conversation, you must only extract the user parameter from the conversation so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the conversation carefully to figure out the intended user.
If the request is to praise a random user, set user to "*"

#RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


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
Your task right now is to praise {{user}} and make them feel good about themselves.

#INSTRUCTIONS:
The name, bio and posts provided are all from @{{user}}.
Analyze their posts carefully.
Based on the provided information, identify their core vibe and what makes them unique.
Praise them in a way that feels authentic and tailored, not generic.
You can use mystical, rhythmic language, deep insight or casual cool depending on the vibe of @{{user}}.
If their content is funny, match their humor. If they are thoughtful, reflect that. If they're chaotic, celebrate the chaos.
Sprinkle in references to patterns, reggae lyrics, energy, or something cosmic, if it fits.
Keep it short but impactful, a poetic appreciation, a clever compliment, or a deep truth about them.
Break down your praise into 3 short tweets:
First tweet introduces the praise in a glorious way.
Second tweet continues the praise.
Third tweet concludes the praise.
Keep the tweets very short and concise.
You can also reference a couple of their posts in the second and third tweet, but do not include a link in the tweet text, instead put the id in the json field "link".
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


class Praise(IActionStep):
    
  def get_cost(self):
    return 20
    
  def auto_prompt(self):
    channel_url = get_channel_url(self.state.selected_channel)
    user_name, fid = None, None
    if channel_url is None:
      user_name = get_random_user_to_praise(self.state.id)
      fid = get_fid(user_name)
      self.state.request = f'Praise a random user'
    else:
      user_name = get_random_user_to_praise_in_channel(self.state.id, channel_url)
      fid = get_fid(user_name)
      self.state.request = f'Praise a random user in channel /{self.state.selected_channel}'
    self.state.action_params = {'fid': fid, 'user_name': user_name}
    self.state.user = user_name
    self.state.conversation = self.state.request
    
  def parse(self):
    parse_prompt = self.state.format_conversation()
    parse_instructions = self.state.format(parse_user_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_user_schema)
    parsed = {}
    fid, user_name = read_user(params, self.state.fid_origin, default_to_origin=False)
    if user_name == '*' or user_name == '' or user_name is None:
      self.state.log += 'Praise action will pick a random user to praise\n'
      user_name = get_random_user_to_praise(self.state.id)
      fid = get_fid(user_name)
    parsed['fid'] = fid
    parsed['user_name'] = user_name
    self.state.action_params = parsed
    self.state.user = user_name

  def execute(self):
    fid = self.state.action_params['fid']
    user_name = self.state.action_params['user_name']
    if fid is None or user_name is None:
      raise Exception(f"Missing fid/user_name.")
    GetUserProfile(self.state).prepare()
    GetPfpDescrition(self.state).prepare()
    NewAvatar(self.state).prepare()
    prompt = self.state.format(prompt_template)
    instructions = self.state.format(instructions_template)
    result1 = call_llm(prompt, instructions, schema)
    if 'tweet1' not in result1:
      raise Exception('Could not generate a praise')    
    embeds = [self.state.user_new_avatar] if self.state.user_new_avatar is not None else []
    embeds_description = 'New avatar' if self.state.user_new_avatar is not None else None
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
            l = check_link_data({'id':link_id}, self.state.posts_map)
            if l is not None:
              c['embeds'] = [{'fid': l['fid'], 'user_name': l['user_name'], 'hash': l['hash']}]
              c['embeds_description'] = l['text']
        casts.append(c)
    add_cast('tweet2')
    add_cast('tweet3')
    self.state.casts = casts
    log = '<Praise>\n'
    log += 'fid: ' + str(fid) + '\n'
    log += 'user: ' + str(user_name) + '\n'
    log += '</Praise>\n'
    self.state.log += log
