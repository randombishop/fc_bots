import uuid
import os
from bots.i_action_step import IActionStep
from bots.prompts.contexts import conversation_and_request_template
from bots.utils.llms import call_llm
from bots.utils.read_params import read_user
from bots.data.users import get_favorite_users
from bots.utils.images import table_image
from bots.utils.gcs import upload_to_gcs


parse_user_instructions_template = """
INSTRUCTIONS:
You are @{{name}}, a bot programmed to find the favorite accounts of a user.
Based on the provided conversation and request, who should we pull the favorite accounts for?
Your goal is not to continue the conversation, you must only extract the user parameter from the request so that we can call an API.
Users typically start with @, but not always.
If the request is about self, this or that user, or uses a pronoun, study the conversation carefully to figure out the intended user.

RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


class FavoriteUsers(IActionStep):
  
  def get_cost(self):
    return 20

  def parse(self):
    parse_prompt = self.state.format(conversation_and_request_template)
    parse_instructions = self.state.format(parse_user_instructions_template)
    params = call_llm(parse_prompt, parse_instructions, parse_user_schema)
    parsed = {}
    fid, user_name = read_user(params, self.state.fid_origin, default_to_origin=True)
    parsed['fid'] = fid
    parsed['user_name'] = user_name
    self.state.action_params = parsed
    self.state.user = user_name
  
  def execute(self):
    fid = self.state.action_params['fid']
    user_name = self.state.action_params['user_name']
    if fid is None or user_name is None:
      raise Exception(f"Missing fid or user_name")
    df = get_favorite_users(fid)
    if len(df) < 3:
      raise Exception(f"Not enough data ({len(df)})")
    df.rename(inplace=True, columns={
        'username': 'User',
        'num_recasts': 'Recasts',
        'num_likes': 'Likes',
        'num_replies': 'Replies'
    })
    filename = str(uuid.uuid4())+'.png'
    table_image(df[['User', 'Recasts', 'Likes', 'Replies']], filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    mentions = [int(df.iloc[i]['target_fid']) for i in range(3)]
    mentions_ats = ['@'+df.iloc[i]['User'] for i in range(3)]
    mentions_positions = []
    text = user_name+"'s favorite users are:\n"
    text += "🥇 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += "\n"
    text += "🥈 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += "\n"
    text += "🥉 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += "\n"
    cast = {
      'text': text, 
      'mentions': mentions, 
      'mentions_pos': mentions_positions,
      'mentions_ats': mentions_ats,
      'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"],
      'embeds_description': 'Favorite users'
    }
    casts =  [cast]
    self.state.casts = casts
