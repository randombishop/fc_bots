from bots.i_action_step import IActionStep
from bots.utils.llms import call_llm
from bots.utils.read_params import read_user
from bots.data.bot_history import get_random_user_to_praise, get_random_user_to_praise_in_channel
from bots.data.users import get_fid
from bots.data.channels import get_channel_url
from bots.prepare.get_user_profile import GetUserProfile
from bots.prepare.get_pfp_description import GetPfpDescrition
from bots.prepare.get_user_replies_and_reactions import GetUserRepliesAndReactions
from bots.prepare.get_avatar import GetAvatar

parse_user_instructions_template = """
#INSTRUCTIONS:
You are @{{name}}, a bot programmed to analyze a user profile and generate insights, plus a new avatar.
Based on the provided conversation, which user profile should we analyze?
Your goal is not to continue the conversation, you must only extract the user parameter from the conversation so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the conversation carefully to figure out the intended user.
If the request is targeted to a random user, set user to "*"

#RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


class WhoIs(IActionStep):
    
  def get_cost(self):
    return 20
    
  def auto_prompt(self):
    user_name, fid = None, None
    channel_url = get_channel_url(self.state.selected_channel)
    if self.state.user is not None:
      user_name = self.state.user
      fid = get_fid(user_name)
    if channel_url is None:
      user_name = get_random_user_to_praise(self.state.id)
      fid = get_fid(user_name)
    else:
      user_name = get_random_user_to_praise_in_channel(self.state.id, channel_url)
      fid = get_fid(user_name)
    self.state.request = f'Who is {user_name}?'  
    self.state.action_params = {'fid': fid, 'user_name': user_name}
    self.state.user_fid = fid
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
    self.state.user_fid = fid

  def execute(self):
    fid = self.state.action_params['fid']
    user_name = self.state.action_params['user_name']
    if fid is None or user_name is None:
      raise Exception(f"Missing fid/user_name.")
    GetUserProfile(self.state).prepare()
    GetPfpDescrition(self.state).prepare()
    GetUserRepliesAndReactions(self.state).prepare()
    GetAvatar(self.state).prepare()
    text = self.state.user_casts_description
    if text is None or text == '':
      raise Exception(f"Profile Description is empty")
    embeds = [self.state.user_avatar] if self.state.user_avatar is not None else []
    embeds_description = 'Avatar Img' if self.state.user_avatar is not None else None
    cast = {
      'text': ' ' + text,
      'embeds': embeds,
      'embeds_description': embeds_description,
      'mentions': [fid],
      'mentions_pos': [0],
      'mentions_ats': [f"@{user_name}"]
    }
    self.state.casts = [cast]
    