class CapabilitiesExamples:
  """
  Examples of tasks that can be performed using your tools.
  """
  
  def __init__(self, text: str):
    self.text = text
      
  def __str__(self) -> str:
    return self.text