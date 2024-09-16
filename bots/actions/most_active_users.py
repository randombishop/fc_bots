from dotenv import load_dotenv
load_dotenv()
import uuid
import sys
import os
import pandas
from bots.iaction import IAction
from bots.utils.prompts import instructions_and_request
from bots.utils.llms import call_llm
from bots.utils.read_params import read_channel, read_int
from bots.data.casts_by_user import casts_by_user_sql, casts_by_user_results
from bots.data.bq import dry_run, to_array
from bots.utils.images import user_activity_chart
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts


parse_instructions = """
INSTRUCTIONS:
Extract the parameters from the user query to find the most active users in a channel over a given number of days.
Your goal is not to answer the query, you only need to extract the parameters channel and num_days.

PARAMETERS:
* channel, text, required.
* num_days, integer, optional, defaults to 1

RESPONSE FORMAT:
{{
  "channel": ...,
  "num_days": ...
}}
(if the user query can not be mapped to the function, return a json with an error message)
"""


class MostActiveUsers(IAction):

  def parse(self, input, fid_origin=None):
    prompt = instructions_and_request(parse_instructions, input)
    self.params = call_llm(prompt)
    self.channel = read_channel(self.params)
    self.num_days = read_int(self.params, 'num_days', 7, 3, 15)
    self.max_rows = read_int(self.params, 'max_rows', 10, 1, 10)
    
  def get_cost(self):
    sql = casts_by_user_sql(self.channel, self.num_days, self.max_rows)
    test = dry_run(sql)
    self.cost = test['cost']
    return self.cost

  def execute(self):
    users = casts_by_user_results(self.channel, self.num_days, self.max_rows)
    if len(users) == 0:
      raise Exception("Query returned 0 rows")
    self.data = to_array(users)
    return self.data
  
  def get_casts(self, intro=''):
    df = pandas.DataFrame(self.data['values'], columns=self.data['columns'])
    rename_cols = {x: x.replace('casts-', '') for x in df.columns}
    rename_cols['user_name']='User'
    df.rename(columns=rename_cols, inplace=True)      
    filename = str(uuid.uuid4())+'.png'
    user_activity_chart(df, filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    mentions = [int(df.iloc[i]['fid']) for i in range(3)]
    mentions_ats = ['@'+df.iloc[i]['User'] for i in range(3)]
    mentions_positions = []
    print(f"Mentioned users: {mentions_ats}")
    print(f"Mentioned fid: {mentions}")
    text = "The most active users are: \n"
    text += "🥇 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += f" : {df.iloc[0]['casts_total']} casts.\n"
    text += "🥈 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += f" : {df.iloc[1]['casts_total']} casts.\n"
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
  action.parse(input)
  print(f"Channel: {action.channel}")    
  print(f"Num days: {action.num_days}")
  print(f"Max rows: {action.max_rows}")
  cost = action.get_cost()
  print(f"Cost: {cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
  