FIELDS = ['request','fid_origin', 'parent_hash', 'attachment_hash', 'root_parent_url']

class BotState:
  
  def __init__(self):
    self.data = {}

  def __setitem__(self, key, value):
    if key in FIELDS:
      self.data[key] = value
    else:
      raise ValueError(f"Invalid field: {key}")
  
  def __setattr__(self, key, value):
    self.__setitem__(key, value)
    
  def __getitem__(self, key):
    if key in FIELDS:
      if key in self.data and self.data[key] is not None:
        return self.data[key]
      else:
        return ''
    else:
      raise ValueError(f"Invalid field: {key}")
    
  def __getattr__(self, key):
    return self.__getitem__(key)

  