import re


DEFAULT_TEMPLATE = """
#NAME
{{name}}

#ACTIONS
{{actions}}

#REQUEST
{{request}}

#PARAMS
fid_origin={{fid_origin}}, parent_hash={{parent_hash}}, attachment_hash={{attachment_hash}}, root_parent_url={{root_parent_url}}

#BIO
{{bio}}

#CHANNEL
{{channel}}

#CONVERSATION
{{conversation}}

#LORE
{{lore}}

#TIME
{{time}}

#STYLE
{{style}}

#SELECTED ACTION
{{selected_action}}
"""


class BotState:
  
  def __init__(self):
    # From initialization
    self.name = ''
    self.request = ''
    self.fid_origin = None
    self.parent_hash = None
    self.attachment_hash = None
    self.root_parent_url = None
    # From wakeup
    self.actions = ''
    self.bio = ''
    self.channel = ''
    self.conversation = ''
    self.lore = ''
    self.time = ''
    self.style = ''
    # From action plan
    self.selected_action = None
    
  def set(self, key, value):
    if hasattr(self, key):
      setattr(self, key, value)
    else:
      raise ValueError(f"Invalid field: {key}")
    
  def format(self, template=DEFAULT_TEMPLATE):
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
