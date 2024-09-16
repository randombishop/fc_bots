from dotenv import load_dotenv
load_dotenv()
import sys
import uuid
import os
import pandas
from bots.iaction import IAction
from bots.utils.prompts import instructions_and_request
from bots.utils.llms import call_llm
from bots.utils.read_params import read_fid
from bots.data.reactions import favorite_users_sql, favorite_users_results
from bots.data.bq import dry_run, to_array
from bots.utils.images import table_image
from bots.utils.gcs import upload_to_gcs
from bots.utils.check_casts import check_casts


parse_instructions = """
INSTRUCTIONS:
Extract the user name from the query.
Your goal is not to answer the query, you only need to extract the user parameter.
For example, if the user query is "Who are @alice.eth's favorite users?", the user is "alice.eth".

PARAMETER:
* user, text or integer, required.

RESPONSE FORMAT:
{{
  "user": ...
}}
(if the user query can not be mapped to the function, return a json with an error message)
"""


class FavoriteUsers(IAction):
  
  def parse(self, input, fid_origin=None):
    prompt = instructions_and_request(parse_instructions, input, fid_origin)
    self.params = call_llm(prompt)
    self.fid = read_fid(self.params)

  def get_cost(self):
    sql = favorite_users_sql(self.fid)
    test = dry_run(sql)
    self.cost = test['cost']
    return self.cost

  def execute(self):
    users = favorite_users_results(self.fid)
    if len(users) < 3:
      raise Exception(f"Not enough data ({len(users)})")
    self.data = to_array(users)
    return self.data
    
  def get_casts(self, intro=''):
    df = pandas.DataFrame(self.data['values'], columns=self.data['columns'])
    df.rename(inplace=True, columns={
        'username': 'User',
        'num_recasts': 'Recasts',
        'num_likes': 'Likes',
        'num_replies': 'Replies'
    })
    filename = str(uuid.uuid4())+'.png'
    table_image(df[['User', 'Recasts', 'Likes', 'Replies']], filename)
    upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
    os.remove(filename)
    mentions = [int(df.iloc[i]['target_fid']) for i in range(3)]
    mentions_ats = ['@'+df.iloc[i]['User'] for i in range(3)]
    mentions_positions = []
    print(f"Mentioned users: {mentions_ats}")
    print(f"Mentioned fid: {mentions}")
    text = "The winners are... \n"
    text += "🥇 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += "\n"
    text += "🥈 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += "\n"
    text += "🥉 "
    mentions_positions.append(len(text.encode('utf-8')))
    text += "\n"
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
  action = FavoriteUsers()
  action.parse(input)
  print(f"FID: {action.fid}")
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")
