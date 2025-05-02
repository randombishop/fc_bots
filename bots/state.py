from bots.kit_interface.variable import Variable
from bots.kit_entrypoint.fetch import Fetch
from bots.kit_entrypoint.prepare import Prepare


class State:
  
  def __init__(self):
    self.bot_id = None
    self.name = None
    self.character = None
    self.mode = None
    self.request = None
    self.fid_origin = None
    self.parent_hash = None
    self.attachment_hash = None
    self.root_parent_url = None
    self.blueprint = None
    self.variables = {}
  
  def get_variable(self, name: str):
    if name in self.variables:
      return self.variables[name].value
    else:
      return None
  
  def set_variable(self, variable: Variable):
    self.variables[variable.name] = variable
      
  def fetch(self, method: str, str_params: dict, var_params: dict, variable_name: str, variable_description: str):
    fetch_entrypoint = Fetch(self)
    pass
  
  def prepare(self, method: str, str_params: dict, var_params: dict, variable_name: str, variable_description: str):
    prepare_entrypoint = Prepare(self)
    pass
