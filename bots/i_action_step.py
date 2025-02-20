class IActionStep:
    
  def __init__(self, state):
    self.state = state
  
  def get_prepare_steps(self):
    return []

  def get_cost(self):
    """Calculate and return the cost of executing the action."""
    raise NotImplementedError("Step doesn't implement get_cost")

  def auto_prompt(self):
    """Generate a prompt for the action when there is no explicit request."""
    raise NotImplementedError("Step doesn't implement auto_prompt")
      
  def parse(self):
    """Parse the parameters from the state."""
    raise NotImplementedError("Step doesn't implement parse")
  
  def execute(self):
    """Pull the data needed by the action."""
    raise NotImplementedError("Step doesn't implement execute")
