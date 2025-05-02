class Avatar:
  """
  Represents an avatar newly created based on a user profile and their original PFP.
  """
  
  def __init__(self, prompt: str, url: str):
    self.prompt = prompt
    self.url = url
      
  def __str__(self) -> str:
    return self.url