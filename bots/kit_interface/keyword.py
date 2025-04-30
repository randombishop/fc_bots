class Keyword:
  """
  Represents a single keyword to be used for searching casts.
  """
  
  def __init__(self, keyword: str):
    self.keyword = keyword
      
  def __str__(self) -> str:
    return f"#Keyword:\n{self.keyword}"