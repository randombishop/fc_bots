class IAction:
    
  def __init__(self):
    self.params = None
    self.data = None
    self.casts = None

  def set_params(self, params):
    self.params = params

  def parse(self, input, fid_origin=None, parent_hash=None):
    """Parse the prompt and set the params."""
    raise NotImplementedError("Action doesn't implement parse")

  def get_cost(self):
    """Calculate and return the cost of executing the action."""
    raise NotImplementedError("Action doesn't implement get_cost")

  def execute(self):
    """Execute the action."""
    raise NotImplementedError("Action doesn't implement execute")

  def get_casts(self, intro=''):
    """Return the associated casts."""
    raise NotImplementedError("Action doesn't implement get_casts")