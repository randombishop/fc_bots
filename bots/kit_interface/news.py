class News:
  """
  Represents a news story.
  """
  
  def __init__(self, story: str, link: str):
    self.story = story
    self.link = link
      
  def __str__(self) -> str:
    return f"#News: {self.link}\n{self.story}"  