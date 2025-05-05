from bots.kit_interface.variable import Variable
from bots.kit_entrypoint.fetch import Fetch
from bots.kit_entrypoint.prepare import Prepare
from bots.kit_entrypoint.memorize import Memorize
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
    self.todo = []
    
  def set_variable(self, variable: Variable):
    """
    Sets a variable in the state
    
    Args:
      variable: Variable - The variable to set
    """
    self.variables[variable.name] = variable
  
  def get_variable(self, name: str):
    """
    Gets a variable from the state
    
    Args:
      name: str - The name of the variable to get
    """
    if name in self.variables:
      return self.variables[name]
    else:
      return None
    
  def get_implementation(self, tool: str):
    if tool == 'fetch':
      return Fetch(self)
    elif tool == 'prepare':
      return Prepare(self)
    elif tool == 'memorize':
      return Memorize(self)
    else:
      raise ValueError(f"Invalid tool: {tool}")
  
  def execute(self, tool: str, method: str, str_params: dict, var_params: dict, variable_name: str, variable_description: str):
    """
    Executes a method from the Fetch, Prepare or Memorize suite of tools
    
    Args:
      tool: str - The tool implementation to use (fetch or prepare) (*required)
      method: str - The method to execute (see the tool implementation for details) (*required)
      str_params: dict - The string parameters to pass to the method (optional)
      var_params: dict - The variable references to pass to the method, these must be available in self.variables (optional)
      variable_name: str - The name of the variable to set with the result of the method (optional)
      variable_description: str - The description of the obtained variable (optional)
      
    Returns:
      The result of the executed method
    """
    params = combine_params(self, str_params, var_params)
    object = self.get_implementation(tool)
    func = get_function(object, method)
    check_params(func, params)
    result = func(**params)
    if result is not None and variable_name is not None:
      variable = Variable(variable_name, variable_description, result)
      self.set_variable(variable)
    return result

