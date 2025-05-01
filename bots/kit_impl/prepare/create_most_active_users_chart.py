import uuid
import os
from bots.kit_interface.most_active_users import MostActiveUsers
from bots.kit_interface.most_active_users_chart import MostActiveUsersChart
from bots.utils.images import user_activity_chart
from bots.utils.gcs import upload_to_gcs


def create_most_active_users_chart(data: MostActiveUsers) -> MostActiveUsersChart:
  if len(data.df) == 0:
    raise Exception("Empty dataframe")
  filename = str(uuid.uuid4())+'.png'
  user_activity_chart(data.df, filename)
  upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
  os.remove(filename)
  url = f"https://fc.datascience.art/bot/main_files/{filename}"
  return MostActiveUsersChart(url)
