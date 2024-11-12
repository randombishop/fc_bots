from dotenv import load_dotenv
load_dotenv()
import uuid
import sys
import os
from bots.iaction import IAction
from bots.utils.prompts import instructions_and_request
from bots.utils.llms import call_llm
from bots.utils.read_params import read_channel
from bots.data.users import get_top_daily_casters
from bots.utils.images import user_activity_chart
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts


parse_instructions = """
INSTRUCTIONS:
Find the channel in the user input. 
Your goal is not to answer the request, you only need to extract the channel parameter.
The query doesn't need to match a specific format, your job is to guess the channel that the user is asking for.

PARAMETERS:
* channel, text, required.

RESPONSE FORMAT:
{{
  "channel": ...
}}
"""


class MostActiveUsers(IAction):

  def set_input(self, input):
    prompt = instructions_and_request(parse_instructions, input)
    params = call_llm(prompt)
    self.input = input
    self.set_params(params)
  
  def set_params(self, params):
    self.channel = read_channel(params)

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


if __name__ == "__main__":
  input = sys.argv[1] 
  action = MostActiveUsers()
  action.set_input(input)
  print(f"Channel: {action.channel}")    
  cost = action.get_cost()
  print(f"Cost: {cost}")
  action.get_data()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
  