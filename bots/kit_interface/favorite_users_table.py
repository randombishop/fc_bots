class FavoriteUsersTable:
  """
  Table image URL showing the favorite users in a channel.
  """
  
  def __init__(self, url: str):
    self.url = url
      
  def __str__(self) -> str:
    return f"#FavoriteUsersTable\nurl -> {self.url}"