class ImageDescription:
  """
  Represents a description of an image.
  """
  
  def __init__(self, url: str, description: str):
    self.url = url
    self.description = description
      
  def __str__(self) -> str:
    return f"""#ImageDescription (url -> {self.url})
    {self.description}"""