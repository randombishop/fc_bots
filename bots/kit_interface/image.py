class Image:
  """
  Represents an image newly created.
  """
  
  def __init__(self, prompt: str, url: str):
    self.prompt = prompt
    self.url = url
      
  def __str__(self) -> str:
    return f"{self.prompt}\n-> {self.url}"