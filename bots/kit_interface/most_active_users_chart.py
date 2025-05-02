class MostActiveUsersChart:
  """
  Chart image URL showing the most active users in a channel.
  """
  
  def __init__(self, url: str):
    self.url = url
      
  def __str__(self) -> str:
    return self.url