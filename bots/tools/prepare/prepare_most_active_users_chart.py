import uuid
import os
from langchain.agents import Tool
from bots.utils.images import user_activity_chart
from bots.utils.gcs import upload_to_gcs


def prepare(input):
  state = input.state
  df = state.get('data_most_active_users')
  if len(df) == 0:
    raise Exception("Empty dataframe")
  filename = str(uuid.uuid4())+'.png'
  user_activity_chart(df, filename)
  upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
  os.remove(filename)
  most_active_users_chart = f"https://fc.datascience.art/bot/main_files/{filename}"
  return {
    'most_active_users_chart': most_active_users_chart
  }


PrepareMostActiveUsersChart = Tool(
  name="PrepareMostActiveUsersChart",
  description="Prepare the most active users chart",
  metadata={
    'inputs': ['data_most_active_users'],
    'outputs': ['most_active_users_chart']
  },
  func=prepare
)
