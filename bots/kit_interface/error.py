class Error:
  """
  Reports a runtime error.
  """
  
  def __init__(self, message: str, stacktrace: str):
    self.message = message
    self.stacktrace = stacktrace
      
  def __str__(self) -> str:
    return self.message
  
