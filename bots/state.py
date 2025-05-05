from bots.kit_interface.variable import Variable
from bots.kit_entrypoint.fetch import Fetch
from bots.kit_entrypoint.prepare import Prepare
from bots.utils.functions import combine_params, get_function, check_params


class State:
  
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
  
  def get_variable(self, name: str):
    if name in self.variables:
      return self.variables[name].value
    else:
      return None
  
  def set_variable(self, variable: Variable):
    self.variables[variable.name] = variable

  def _execute(self, object, method, str_params: dict, var_params: dict, variable_name: str, variable_description: str):
    params = combine_params(self, str_params, var_params)
    func = get_function(object, method)
    check_params(func, params)
    result = func(**params)
    if result is not None:
      variable = Variable(variable_name, variable_description, result)
      self.set_variable(variable)
    return result
  
  def fetch(self, method: str, str_params: dict, var_params: dict, variable_name: str, variable_description: str):
    fetch_entrypoint = Fetch(self)
    return self._execute(fetch_entrypoint, method, str_params, var_params, variable_name, variable_description)
  
  def prepare(self, method: str, str_params: dict, var_params: dict, variable_name: str, variable_description: str):
    prepare_entrypoint = Prepare(self)
    return self._execute(prepare_entrypoint, method, str_params, var_params, variable_name, variable_description)
