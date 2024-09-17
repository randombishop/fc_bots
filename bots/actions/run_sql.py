from dotenv import load_dotenv
load_dotenv()
import uuid
import sys
from bots.iaction import IAction
from bots.utils.llms import call_llm
from bots.utils.prompts import instructions_and_request
from bots.data.bq import dry_run, sql_to_gcs

instructions = """
INSTRUCTIONS:
Check that the following query is an actual SQL statement, that it's read only, and that is doesn't have any security issues or risks if sent to BigQuery.
Output your check as a json object.

RESPONSE FORMAT:
{
  "ok": true/false
}
"""


class RunSql(IAction):

  def set_input(self, input):
    prompt = instructions_and_request(instructions, input)
    result = call_llm(prompt)
    if 'ok' not in result or not result['ok']:
      raise Exception('The query is not a valid read-only SQL.')
    self.sql = input
  
  def set_params(self, params):
    self.sql = params['sql']  

  def get_cost(self):
    test = dry_run(self.sql)
    self.cost = test['cost']
    return self.cost
    
  def get_data(self):
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
  input = sys.argv[1]
  action = RunSql()
  action.set_input(input)
  print(f"Sql: {action.sql}")
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.get_data()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
