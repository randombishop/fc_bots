class IAction:
    
  def __init__(self):
    self.fid_origin = None
    self.parent_hash = None
    self.data = None
    self.casts = None

  def set_fid_origin(self, fid_origin):
    self.fid_origin = fid_origin

  def set_parent_hash(self, parent_hash):
    self.parent_hash = parent_hash

  def set_input(self, input):
    """Use natural language input to set the params."""
    raise NotImplementedError("Action doesn't implement parse")
  
  def set_params(self, params):
    """Use dictionary params."""
    raise NotImplementedError("Action doesn't implement parse")

  def get_cost(self):
    """Calculate and return the cost of executing the action."""
    raise NotImplementedError("Action doesn't implement get_cost")

  def get_data(self):
    """Pull the data needed by the action."""
    raise NotImplementedError("Action doesn't implement get_data")

  def get_casts(self, intro=''):
    """Return the associated casts."""
    raise NotImplementedError("Action doesn't implement get_casts")