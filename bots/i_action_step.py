class IActionStep:
    
  def __init__(self):
    self.fid_origin = None
    self.root_parent_url = None
    self.data = None
    self.casts = None

  def set_fid_origin(self, fid_origin):
    self.fid_origin = int(fid_origin) if fid_origin is not None else None
    
  def set_root_parent_url(self, root_parent_url):
    self.root_parent_url = root_parent_url

  def set_input(self, input):
    """Use natural language input to set the params."""
    raise NotImplementedError("Action doesn't implement set_input")
  
  def set_params(self, params):
    """Use dictionary params."""
    raise NotImplementedError("Action doesn't implement set_params")

  def get_cost(self):
    """Calculate and return the cost of executing the action."""
    raise NotImplementedError("Action doesn't implement get_cost")

  def get_data(self):
    """Pull the data needed by the action."""
    raise NotImplementedError("Action doesn't implement get_data")

  def get_casts(self, intro=''):
    """Return the associated casts."""
    raise NotImplementedError("Action doesn't implement get_casts")
  
  def run(self, intro=''):
    """Run the action."""
    self.get_cost()
    self.get_data()
    self.get_casts(intro)
    
  def print(self):
    attrs = ['fid', 'user_name', 'channel', 'keyword', 'category', 'search', 'criteria', 'text', 'question', 'cost']
    s = '\n'
    s += ('-'*64) + '\n'
    s += f"{self.input}>>>\n"
    s += f"  action: {self.__class__.__name__ }\n"
    for attr in attrs:
      if hasattr(self, attr): 
        s += f"  {attr}: {getattr(self, attr)}\n"
    if hasattr(self, 'casts') and self.casts is not None: 
      casts = self.casts
      s += "<<< casts:\n"
      for c in casts:
        s+= f"{c}\n"
    s += ('-'*64)
    s += '\n'
    print(s)
