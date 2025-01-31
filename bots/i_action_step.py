class IActionStep:
    
  def __init__(self, state):
    self.state = state
    
  def get_cost(self):
    """Calculate and return the cost of executing the action."""
    raise NotImplementedError("Action doesn't implement get_cost")
      
  def parse(self):
    """Parse the parameters from the state."""
    raise NotImplementedError("Action doesn't implement set_params")
  
  def execute(self):
    """Pull the data needed by the action."""
    raise NotImplementedError("Action doesn't implement get_data")
