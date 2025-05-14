from bots.kit_interface.variable import Variable


class BaseState:
  
  def __init__(self):
    self.bot_id = None
    self.bot_name = None
    self.character = None
    self.mode = None
    self.request = None
    self.fid_origin = None
    self.parent_hash = None
    self.attachment_hash = None
    self.root_parent_url = None
    self.blueprint = None
    self.variables = {}
    self.plan = None
    self.todo = []
    self.iterations = 0
    self.composed = False
    self.checked = False
    self.casts = None
    self.valid = False
    self.memorized = False
    self.like = False

  def get_bot_id(self):
    return self.bot_id
  
  def set_variable(self, variable: Variable):
    self.variables[variable.name] = variable
  
  def get_variable(self, name: str) -> Variable | None:
    if name in self.variables:
      return self.variables[name]
    else:
      return None
    
  def get_variable_types(self):
    ans = {}
    for variable in self.variables.values():
      if variable.value.__class__.__name__ not in ans:
        ans[variable.value.__class__.__name__] = 0
      ans[variable.value.__class__.__name__] += 1
    return ans
    
  def get_variable_values_by_type(self, variable_type: str):
    return [x.value for x in self.variables.values() if x.value.__class__.__name__==variable_type]
  
  def has_variable_value_with_type(self, variable_type: str):
    return len(self.get_variable_values_by_type(variable_type)) > 0
  
  def get_last_variable_value_by_type(self, variable_type: str):
    vars = self.get_variable_values_by_type(variable_type)
    if len(vars) > 0:
      return vars[-1]
    else:
      return None
  
  def get_selected_channel_id(self):
    var = self.get_variable('selected_channel')
    if var is not None:
      return var.value
    else:
      return None
    
  def get_selected_user_id(self):
    var = self.get_variable('selected_user')
    if var is not None:
      return var.value
    else:
      return None
    
  def get_selected_intent(self):
    if self.plan is not None and 'intent' in self.plan:
      return self.plan['intent']
    else:
      return None

  def should_like(self):
    return self.like
  
  def is_valid(self):
    return self.valid
  
  def get_casts(self):
    return self.casts