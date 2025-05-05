import inspect
import traceback


def combine_params(state, str_params, var_params):
  params = {}
  if str_params is not None:
    params.update(str_params)
  if var_params is not None:
    for key, ref in var_params.items():
      v = state.get_variable(ref)
      if v is None:
        raise ValueError(f"Variable {ref} not found")
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
      if not isinstance(actual_value, expected_type):
        raise TypeError(f"Parameter {param_name} expects type {expected_type}, got {type(actual_value)}")
      

def validate_function(input):
  config = input['config']
  tool = config['tool']
  if tool not in ['fetch', 'prepare']:
    raise ValueError(f"Invalid tool: {tool}")
  method = config['method']
  str_params = config['str_params'] if 'str_params' in config else None
  var_params = config['var_params'] if 'var_params' in config else None
  variable_name = config['variable_name']
  variable_description = config['variable_description']
  return tool, method, str_params, var_params, variable_name, variable_description


def exec_function(state, tool, method, str_params, var_params, variable_name, variable_description):
  try:
    return state.execute(tool, method, str_params, var_params, variable_name, variable_description)
  except Exception as e:
    print(traceback.format_exc())
    return {
      'error': str(e),
      'stacktrace': traceback.format_exc().splitlines()
    }