class Variable:
  """
  Represents a state variable.
  """
  
  def __init__(self, name: str, description: str, value):
    self.name = name
    self.description = description
    self.value = value

  def get_type(self):
    try:
      return self.value.__class__.__name__
    except:
      return str(type(self.value))

  def __str__(self) -> str:
    try:
      variable_type = self.value.__class__.__name__
    except:
      variable_type = type(self.value)
    variable_value = str(self.value)
    if len(variable_value) > 50:
      variable_value = variable_value[:47] + '...'
      variable_value = variable_value.replace('\n', ' ')
    return f"{self.name} ({variable_type}) -> {self.description} -> {variable_value}"