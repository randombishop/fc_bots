class IPlanStep:
    
  def __init__(self, state):
    self.state = state
  
  def plan(self):
    """Execute the planning step."""
    raise NotImplementedError("Step doesn't implement plan")
