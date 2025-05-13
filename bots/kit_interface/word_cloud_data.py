class WordCloudData:
  """
  Data used to render a word cloud.
  Contains a string and the dictionary of word counts.
  """
  
  def __init__(self, text: str, word_counts: dict):
    self.text = text
    self.word_counts = word_counts
    
  def __str__(self) -> str:
    return f"{len(self.word_counts)} words"