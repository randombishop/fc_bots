class SearchPhrase:
  """
  Represents a search phrase to be used for fetching casts.
  """
  
  def __init__(self, search: str):
    self.search = search
      
  def __str__(self) -> str:
    return self.search