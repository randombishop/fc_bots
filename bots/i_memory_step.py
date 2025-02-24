class IMemoryStep:
    
  def __init__(self, state):
    self.state = state
    
  def recall(self):
    """Recall a memory."""
    raise NotImplementedError("Step doesn't implement recall")
  
  def record(self):
    """Record a memory."""
    raise NotImplementedError("Step doesn't implement record")
