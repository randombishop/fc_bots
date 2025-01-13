from dotenv import load_dotenv
load_dotenv()
import uuid
import sys
import os
from bots.iaction import IAction
from bots.utils.llms import call_llm
from bots.utils.read_params import read_channel
from bots.data.users import get_top_daily_casters
from bots.utils.images import user_activity_chart
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts


parse_instructions = """
INSTRUCTIONS:
You are @dsart, a bot programmed to list the most active users in a social media channel.
Based on the provided conversation, which channel should we look at? 
Your goal is not to continue the conversation, you must only extract the channel parameter.
Channels typically start with /, but not always.

RESPONSE FORMAT:
{
  "channel": ...
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "channel":{"type":"STRING"}
  }
}


class MostActiveUsers(IAction):

  def set_input(self, input):
    params = call_llm(input, parse_instructions, parse_schema)
    self.input = input
    self.set_params(params)
  
  def set_params(self, params):
    self.channel = read_channel(params, current_channel=self.root_parent_url, default_to_current=True)

  def get_cost(self):
    self.cost = 20
    return self.cost

  def get_data(self):
    users = get_top_daily_casters(self.channel)
    if len(users) == 0:
      raise Exception("Query returned 0 rows")
    self.data = users
  
  def get_casts(self, intro=''):
    df = self.data
    filename = str(uuid.uuid4())+'.png'
    user_activity_chart(df, filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    num_mentions = min(len(df), 3)
    mentions = [int(df.iloc[i]['fid']) for i in range(num_mentions)]
    mentions_ats = ['@'+df.iloc[i]['User'] for i in range(num_mentions)]
    mentions_positions = []
    text = "The most active users are: \n"
    text += "🥇 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += f" : {df.iloc[0]['casts_total']} casts.\n"
    if num_mentions > 1:
      text += "🥈 "
      mentions_positions.append(len(text.encode('utf-8')))
      text += f" : {df.iloc[1]['casts_total']} casts.\n"
    if num_mentions > 2:
      text += "🥉 "
      mentions_positions.append(len(text.encode('utf-8')))
      text += f" : {df.iloc[2]['casts_total']} casts.\n"
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

