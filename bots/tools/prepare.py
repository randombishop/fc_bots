from langchain.agents import Tool
from langsmith import traceable
from bots.utils.functions import validate_function, exec_function


def _prepare(input):
  state = input['state']
  tool, method, str_params, var_params, variable_name, variable_description = validate_function(input)
  @traceable(run_type="chain", name=method)
  def _exec_function(str_params, var_params):
    return exec_function(state, tool, method, str_params, var_params, variable_name, variable_description)
  _exec_function(str_params, var_params)
  return state.get_variable(variable_name)


prepare = Tool(
  name="prepare",
  description="Execute a prepare method",
  func=_prepare
)