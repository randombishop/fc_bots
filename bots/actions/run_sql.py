from dotenv import load_dotenv
load_dotenv()
import json
import sys
from bots.iaction import IAction
from bots.utils.read_params import read_string
from bots.data.bq import dry_run


class RunSql(IAction):

  def __init__(self, params):
    super().__init__(params)
    self.sql = read_string(params, 'sql', '', 1000)
    
  def get_cost(self):
    test = dry_run(self.sql)
    if 'error' in test:
      self.error = test['error']
      return 0
    else:
      self.cost = test['cost']
      return self.cost
    
  def execute(self):
    return None
    
  def get_casts(self, intro=''):
    return None


if __name__ == "__main__":
  sql = sys.argv[1]
  params = {'sql': sql}
  action = RunSql(params)
  print(f"Sql: {action.sql}")
  cost = action.get_cost()
  print(f"Cost: {cost}")
  if action.error is None:
    action.execute()
    print(f"Result: {action.result}")
    if action.result is not None:
      action.get_casts()
      print(f"Casts: {action.casts}")
  if action.error:  
    print(f"Error: {action.error}")