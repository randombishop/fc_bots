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
    self.cost = test['cost']
    return self.cost
    
  def execute(self):
    filename = str(uuid.uuid4())
    folder = 'csv'
    result = sql_to_gcs(self.sql, folder, filename)
    self.data = {      
      'id': filename,
      'total_rows': result['total_rows']
    }
    return self.data
    
  def get_casts(self, intro=''):
    if self.data['total_rows'] == 0:
      self.casts = [{'text': 'Your SQL query returned 0 rows.'}]
    else:
      text = f"Your SQL query returned {self.data['total_rows']} rows.\n"
      text += f"Here is a link to the results: https://fc.datascience.art/bot/tmp_files/{self.data['id']}.csv"
      self.casts =  [{'text': text}]
    return self.casts

if __name__ == "__main__":
  sql = sys.argv[1]
  params = {'sql': sql}
  action = RunSql(params)
  print(f"Sql: {action.sql}")
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
