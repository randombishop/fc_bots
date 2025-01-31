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
  
  def __init__(self, name=None, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None):
    # 1. Initialization
    self.name = name
    self.request = request
    self.fid_origin = int(fid_origin) if fid_origin is not None else None
    self.parent_hash = parent_hash
    self.attachment_hash = attachment_hash
    self.root_parent_url = root_parent_url
    # 2. Wake up
    self.actions = ''
    self.bio = ''
    self.channel = ''
    self.conversation = ''
    self.lore = ''
    self.time = ''
    self.style = ''
    # 3. Plan actions
    self.selected_action = None
    # 4. Execute actions
    self.action_params = None
    self.casts = []
    # 5. Think
    self.like = False
    self.reply = False
    
    
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
  
  def debug_action(self):
    if self.selected_action is None or self.action_params is None:
      return 'no parameters were parsed'
    attrs = ['fid', 'user_name', 'channel', 'keyword', 'category', 'search', 'criteria', 'text', 'question', 'cost']
    s = ('-'*64) + '\n'
    s += f"{self.selected_action}\n"
    for attr in attrs:
      if attr in self.action_params and self.action_params[attr] is not None: 
        s += f"  {attr}: {self.action_params[attr]}\n"
    if hasattr(self, 'casts') and self.casts is not None: 
      casts = self.casts
      s += "Casts:\n"
      for c in casts:
        s+= f"  {c}\n"
    s += ('-'*64)
    s += '\n'
    print(s)
