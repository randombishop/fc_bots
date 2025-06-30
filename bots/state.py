from bots.utils.base_state import BaseState
from bots.kit_interface.variable import Variable
from bots.kit_entrypoint.fetch import Fetch
from bots.kit_entrypoint.prepare import Prepare
from bots.kit_entrypoint.miniapps import MiniApps
from bots.utils.functions import combine_params, get_function, check_params


class State(BaseState):
  
  def __init__(self):
    super().__init__()
    
  def get_implementation(self, tool: str) -> Fetch | Prepare | MiniApps:
    """
    Instantiates a tool implementation
    
    Args:
      tool: str - The tool implementation to use (fetch, prepare or miniapps)
      
    Returns:
      The tool implementation
    """
    if tool == 'fetch':
      return Fetch(self)
    elif tool == 'prepare':
      return Prepare(self)
    elif tool == 'miniapps':
      return MiniApps(self)
    else:
      raise ValueError(f"Invalid tool: {tool}")
  
  def execute(self, tool: str, method: str, str_params: dict, var_params: dict, variable_name: str, variable_description: str):
    """
    Executes a method from the Fetch, Prepare or Memorize suites of tools
    and stores the result in the state variables dictionary.
    
    Args:
      tool: str - The tool implementation to use (fetch or prepare) (*required)
      method: str - The method to execute (see the tool implementation for details) (*required)
      str_params: dict - The string parameters to pass to the method (optional)
      var_params: dict - The variable references to pass to the method, these must be available in self.variables (optional)
      variable_name: str - The name of the recipient variable containing the result of the method (*required)
      variable_description: str - The description of the obtained variable (optional)
      
    Returns:
      The result of the executed method
    """
    params = combine_params(self.variables, str_params, var_params)
    object = self.get_implementation(tool)
    func = get_function(object, method)
    check_params(func, params)
    result = func(**params)
    if result is not None:
      variable = Variable(variable_name, variable_description, result)
      self.set_variable(variable)
    return result

