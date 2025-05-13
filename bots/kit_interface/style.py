class Style:
  """
  Stores the bot's writing style.
  """
  
  def __init__(self, style: list[str]):
    self.style = style
      
  def __str__(self) -> str:
    return '\n'.join(self.style)
