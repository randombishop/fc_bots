import re


class BotState:
  
  def __init__(self):
    # From initialization
    self.request = ''
    self.fid_origin = None
    self.parent_hash = None
    self.attachment_hash = None
    self.root_parent_url = None
    # From wakeup
    self.bio = ''
    self.channel = ''
    self.conversation = ''
    self.lore = ''
    self.time = ''
    self.style = ''
    
  def set(self, key, value):
    if hasattr(self, key):
      setattr(self, key, value)
    else:
      raise ValueError(f"Invalid field: {key}")
    
  def format(self, template):
    result = template
    placeholders = re.findall(r'\{\{(\w+)\}\}', template)
    for placeholder in placeholders:
      if not hasattr(self, placeholder):
        raise ValueError(f"Invalid placeholder: {placeholder}")
      value = getattr(self, placeholder)
      if value is None:
        value = ''
      result = result.replace('{{' + placeholder + '}}', value)
    return result
