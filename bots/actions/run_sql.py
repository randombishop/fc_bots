from dotenv import load_dotenv
load_dotenv()
import uuid
import sys
from bots.iaction import IAction
from bots.utils.read_params import read_string
from bots.data.bq import dry_run, sql_to_gcs


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
    filename = str(uuid.uuid4())
    folder = 'run_sql'
    result = sql_to_gcs(self.sql, folder, filename)
    if 'error' in result:
      self.error = result['error']
      return None
    else:
      self.result = {      
        'id': filename,
        'total_rows': result['total_rows']
      }
      return self.result
    
  def get_casts(self, intro=''):
    if self.result is None:
      return None
    else:
      if 'error' in self.result or self.result['total_rows'] == 0:
        return [{
          'text': 'I was unable to process your SQL query.'  
        }]
      else:
        return [{
          'text': f"Your SQL query returned {self.result['total_rows']} rows. Here is a link to the results: https://fc.datascience.art/bot/files/{self.result['id']}.csv"  
        }]


if __name__ == "__main__":
  try:  
    sql = sys.argv[1]
    params = {'sql': sql}
    action = RunSql(params)
    print(f"Sql: {action.sql}")
    cost = action.get_cost()
    print(f"Cost: {cost}")
    action.execute()
    print(f"Result: {action.result}")
    action.get_casts()
    print(f"Casts: {action.casts}")
  except:
    print(f"Error: {action.error}")
  