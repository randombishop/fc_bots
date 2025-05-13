class UserId:
  """
  Represents a farcaster user id.
  """
  
  def __init__(self, fid: int, username: str):
    self.fid = fid
    self.username = username
      
  def __str__(self) -> str:
    return f"@{self.username} ({self.fid})"