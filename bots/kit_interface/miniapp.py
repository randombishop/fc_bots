class MiniApp:
  """
  Represents a link to a Farcaster mini-app.
  """
  
  def __init__(self, url: str):
    self.url = url
      
  def __str__(self) -> str:
    return self.url