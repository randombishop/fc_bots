class UserReactionsDescription:
  """
  Describes a user's replies and reactions.
  """
  
  def __init__(self, text: str, keywords: str):
    self.text = text  
    self.keywords = keywords
      
  def __str__(self) -> str:
    return f"{self.text} ({self.keywords})"