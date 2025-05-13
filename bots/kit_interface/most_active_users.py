import pandas
from bots.kit_interface.channel_id import ChannelId


class MostActiveUsers:
  """
  Data frame containing the most active users in a channel.
  """
  
  def __init__(self, channel_id: ChannelId, df: pandas.DataFrame):
    self.channel_id = channel_id
    self.df = df
      
  def __str__(self) -> str:
    ans = f"Most active users in channel {self.channel_id.channel}\n"
    if len(self.df) > 0:
      rows = self.df.to_dict('records')
      for r in rows:
        ans += f"@{r['User']} posted {r['casts_total']} times\n"
    else:
      ans += "No activity."
    return ans
