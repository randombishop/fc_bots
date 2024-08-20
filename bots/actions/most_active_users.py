from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.read_params import read_channel, read_int
from bots.data.casts_by_user import casts_by_user_sql, casts_by_user_results
from bots.data.bq import dry_run
from bots.utils.prompts import casts_and_instructions
from bots.models.mistral import mistral
from bots.utils.check_links import check_link_data


class MostActiveUsers(IAction):

  def __init__(self, params):
    super().__init__(params)
    self.channel = read_channel(params)
    self.num_days = read_int(params, 'days', 7, 3, 15)
    self.max_rows = read_int(params, 'max_rows', 10, 1, 100)
    
  def get_cost(self):
    sql = casts_by_user_sql(self.channel, self.num_days, self.max_rows)
    print(f"SQL: {sql}")
    test = dry_run(sql)
    if 'error' in test:
      self.error = test['error']
      return 0
    else:
      self.cost = test['cost']
      return self.cost

  def execute(self):
    users = casts_by_user_results(self.channel, self.num_days, self.max_rows)
    self.result = users
    return self.result
  
  def get_casts(self, intro=''):
    casts = []
    self.casts = casts
    return self.casts


if __name__ == "__main__":
  try:  
    channel = sys.argv[1] if len(sys.argv) > 1 else None
    num_days = sys.argv[2] if len(sys.argv) > 2 else None
    max_rows = sys.argv[3] if len(sys.argv) > 3 else None
    params = {'channel': channel, 'days': num_days, 'max_rows': max_rows}
    action = MostActiveUsers(params)
    print(f"Channel: {action.channel}")    
    print(f"Num days: {action.num_days}")
    print(f"Max rows: {action.max_rows}")
    cost = action.get_cost()
    print(f"Cost: {cost}")
    action.execute()
    print(f"Result: {action.result}")
    action.get_casts()
    print(f"Casts: {action.casts}")
  except:
    print(f"Error: {action.error}")