class SourceCode:
  """
  Source code of the bot.
  """   
  
  def __init__(self, code: str):
    self.code = code
      
  def __str__(self) -> str:
    return self.code
  
