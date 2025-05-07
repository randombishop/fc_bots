import inspect
import traceback
import json
from langsmith import traceable
from bots.kit_interface.error import Error
from bots.kit_interface.variable import Variable


def combine_params(variables, str_params, var_params):
  params = {}
  if str_params is not None:
    params.update(str_params)
  if var_params is not None:
    for key, ref in var_params.items():
      if ref not in variables:
        raise ValueError(f"Variable {ref} not found")
      v = variables[ref]
      params[key] = v.value
  return params
  


def get_function(object, method):
  func = getattr(object, method)
  if func is None:
    raise ValueError(f"Method {method} not found")
  return func


def check_params(func, params):
  sig = inspect.signature(func)
  missing_params = [param for param in sig.parameters if param not in params]
  if len(missing_params) > 0:
    raise ValueError(f"Missing required parameters: {missing_params}")
  for param_name, param in sig.parameters.items():
    if param_name in params:
      expected_type = param.annotation
      actual_value = params[param_name]
      if (expected_type!=actual_value) and (not isinstance(actual_value, expected_type)):
        raise TypeError(f"Parameter {param_name} expects type {expected_type}, got {type(actual_value)}")
      

def validate_function(input):
  state = input['state']
  config = input['config']
  tool = config['tool']
  object = state.get_implementation(tool)
  method = config['method']
  func = get_function(object, method)
  str_params = config['str_params'] if 'str_params' in config else None
  var_params = config['var_params'] if 'var_params' in config else None
  params = combine_params(state.variables, str_params, var_params)
  check_params(func, params)
  variable_name = config['variable_name'] if 'variable_name' in config else None
  variable_description = config['variable_description'] if 'variable_description' in config else None
  return tool, method, str_params, var_params, variable_name, variable_description



def exec_function(run_type, input):
  try:
    state = input['state']
    tool, method, str_params, var_params, variable_name, variable_description = validate_function(input)
    params = combine_params(state.variables, str_params, var_params)
    @traceable(run_type=run_type, name=method)
    def _exec_function(params):
      return state.execute(tool, method, str_params, var_params, variable_name, variable_description)
    _exec_function(params)
    if variable_name is not None:
      return state.get_variable(variable_name)
    else:
      return None
  except Exception as e:
    return Error(str(e), traceback.format_exc().splitlines())


def validate_sequence(state, sequence):
  variables = state.variables.copy()
  ans = []
  exception = None
  try:
    for call in sequence:
      tool = call['tool']
      object = state.get_implementation(tool)
      method = call['method']
      func = get_function(object, method)
      str_params = call['str_params'] if 'str_params' in call else None
      var_params = call['var_params'] if 'var_params' in call else None
      params = combine_params(variables, str_params, var_params)
      check_params(func, params)
      ans.append(call)
      sig = inspect.signature(func)
      variable_type = sig.return_annotation
      variable_name = call['variable_name'] if 'variable_name' in call else None
      variable_description = call['variable_description'] if 'variable_description' in call else None
      if variable_name is not None:
        variables[variable_name] = Variable(variable_name, variable_description, variable_type)
  except Exception as e:
    exception = e
  return ans, exception

