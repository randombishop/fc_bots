class IAction:
    
  def __init__(self, params):
    self.params = params

  def get_cost(self):
    """Calculate and return the cost of executing the action."""
    raise NotImplementedError("Action doesn't implement get_cost")

  def execute(self):
    """Execute the action."""
    raise NotImplementedError("Action doesn't implement execute")

  def get_casts(self, intro=''):
    """Return the associated casts."""
    raise NotImplementedError("Action doesn't implement get_casts")