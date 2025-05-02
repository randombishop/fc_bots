class Variable:
  """
  Represents a state variable.
  """
  
  def __init__(self, name: str, description: str, value):
    self.name = name
    self.description = description
    self.value = value
      
  def __str__(self) -> str:
    try:
      variable_type = self.value.__class__.__name__
    except:
      variable_type = type(self.value)
    return f"{self.name} ({variable_type}) -> {self.description}"