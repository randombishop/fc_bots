from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
from bots.iaction import IAction
from bots.utils.read_params import read_fid
from bots.data.reactions import favorite_users_sql, favorite_users_results
from bots.data.bq import dry_run, to_pandas
from bots.utils.images import table_image
from bots.utils.gcs import upload_to_gcs


class FavoriteUsers(IAction):

  def __init__(self, params):
    super().__init__(params)
    self.fid = read_fid(params)
    
  def get_cost(self):
    sql = favorite_users_sql(self.fid)
    test = dry_run(sql)
    if 'error' in test:
      self.error = test['error']
      return 0
    else:
      self.cost = test['cost']
      return self.cost

  def execute(self):
    users = favorite_users_results(self.fid)
    if len(users) < 3:
      raise Exception(f"Not enough data ({len(users)})")
    self.result = users
    return self.result
    
  def get_casts(self, intro=''):
    df = to_pandas(self.result)
    del df['target_fid']
    df.rename(inplace=True, columns={
        'username': 'User',
        'num_recasts': 'Recasts',
        'num_likes': 'Likes',
        'num_replies': 'Replies'
    })
    filename = str(uuid.uuid4())+'.png'
    table_image(df, filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    gold = self.result[0]['username']
    silver = self.result[1]['username']
    bronze = self.result[2]['username']
    print(f"Gold: {gold}, Silver: {silver}, Bronze: {bronze}")
    text = "The winners are... \n"
    text += f"🥇 {gold}\n"
    text += f"🥈 {silver}\n"
    text += f"🥉 {bronze}"
    self.casts =  [{'text': text, 'embeds': [f"https://fc.datascience.art/bot/main_files/{filename}"]}]
    return self.casts


if __name__ == "__main__":
  user = sys.argv[1]
  params = {'user': user}
  action = FavoriteUsers(params)
  print(f"FID: {action.fid}")
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.execute()
  print(f"Result: {action.result}")
  action.get_casts()
  print(f"Casts: {action.casts}")
