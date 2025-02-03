class IThinkStep:
    
  def __init__(self, state):
    self.state = state
  
  def think(self):
    """Execute the thinking step."""
    raise NotImplementedError("Step doesn't implement think")
