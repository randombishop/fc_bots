class IPrepareStep:
    
  def __init__(self, state):
    self.state = state
  
  def execute(self):
    """Execute the preparation step."""
    raise NotImplementedError("Step doesn't implement execute")
