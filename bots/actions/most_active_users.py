from dotenv import load_dotenv
load_dotenv()
import uuid
import sys
import os
import pandas
from bots.iaction import IAction
from bots.utils.read_params import read_channel, read_int
from bots.data.casts_by_user import casts_by_user_sql, casts_by_user_results
from bots.data.bq import dry_run, to_array
from bots.utils.images import user_activity_chart
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts


class MostActiveUsers(IAction):

  def __init__(self, params):
    super().__init__(params)
    self.channel = read_channel(params)
    self.num_days = read_int(params, 'num_days', 7, 3, 15)
    self.max_rows = read_int(params, 'max_rows', 10, 1, 10)
    
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
  channel = sys.argv[1] if len(sys.argv) > 1 else None
  num_days = sys.argv[2] if len(sys.argv) > 2 else None
  max_rows = sys.argv[3] if len(sys.argv) > 3 else None
  params = {'channel': channel, 'num_days': num_days, 'max_rows': max_rows}
  action = MostActiveUsers(params)
  print(f"Channel: {action.channel}")    
  print(f"Num days: {action.num_days}")
  print(f"Max rows: {action.max_rows}")
  cost = action.get_cost()
  print(f"Cost: {cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
  