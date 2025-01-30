import uuid
import os
from bots.iaction import IAction
from bots.utils.llms import call_llm
from bots.utils.read_params import read_user
from bots.data.users import get_favorite_users
from bots.utils.images import table_image
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts


parse_user_instructions = """
INSTRUCTIONS:
You are @dsart, a bot programmed to find the favorite accounts of a user.
Based on the provided conversation, who should we pull the favorite accounts for?
Your goal is not to continue the conversation, you must only extract the user parameter from the conversation so that we can call an API.
Users typically start with @, but not always.
If you're not sure, pick the last token that starts with a @.

RESPONSE FORMAT:
{
  "user": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


class FavoriteUsers(IAction):
  
  def set_input(self, input):
    params = call_llm(input, parse_user_instructions, parse_user_schema)
    self.input = input
    self.set_params(params)
    
  def set_params(self, params):
    self.fid, self.user_name = read_user(params, self.fid_origin, default_to_origin=True)

  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    users = get_favorite_users(self.fid)
    if len(users) < 3:
      raise Exception(f"Not enough data ({len(users)})")
    self.data = users
    return self.data
    
  def get_casts(self, intro=''):
    df = self.data
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
    text = "The winners are... \n"
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
      'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"]
    }
    casts =  [cast]
    check_casts(casts)
    self.casts = casts
    return self.casts
