import uuid
import os
from langchain.agents import Tool
from bots.utils.images import user_activity_chart
from bots.utils.gcs import upload_to_gcs
from bots.data.channels import get_channel_by_url


def prepare_most_active_users_chart(input):
  state = input.state
  df = state.df_most_active_users
  if df is None or len(df) == 0:
    raise Exception("Missing most active users dataframe")
  filename = str(uuid.uuid4())+'.png'
  user_activity_chart(df, filename)
  upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
  os.remove(filename)
  state.most_active_users_chart = f"https://fc.datascience.art/bot/main_files/{filename}"
  return {
    'most_active_users_chart': state.most_active_users_chart
  }


PrepareMostActiveUsersChart = Tool(
  name="PrepareMostActiveUsersChart",
  description="Prepare the most active users chart",
  func=prepare_most_active_users_chart
)
