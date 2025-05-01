class WordCloudImage:
  """
  Image URL showing a word cloud.
  """
  
  def __init__(self, url: str):
    self.url = url
      
  def __str__(self) -> str:
    return f"#WordCloudImage\nurl -> {self.url}"