from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.read_params import read_fid
from fc_bots.bots.data.reactions import favorite_users_sql, favorite_users_results
from bots.data.bq import dry_run
from bots.utils.check_links import check_link_data



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
    self.result = users
    return self.result
    
  def get_casts(self, intro=''):
    casts = []
    return self.casts


if __name__ == "__main__":
  try:  
    username = sys.argv[1]
    params = {'username': username}
    action = FavoriteUsers(params)
    print(f"FID: {action.fid}")
    cost = action.get_cost()
    print(f"Cost: {cost}")
    action.execute()
    print(f"Result: {action.result}")
    action.get_casts()
    print(f"Casts: {action.casts}")
  except:
    print(f"Error: {action.error}")
    
