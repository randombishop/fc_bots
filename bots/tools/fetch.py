from langchain.agents import Tool
import traceback


def exec_fetch(input):
  state = input['state']
  config = input['config']
  method = config['method']
  str_params = config['str_params'] if 'str_params' in config else None
  var_params = config['var_params'] if 'var_params' in config else None
  variable_name = config['variable_name']
  variable_description = config['variable_description']
  try:
    return state.fetch(method, str_params, var_params, variable_name, variable_description)
  except Exception as e:
    print(traceback.format_exc())
    return {
      'error': str(e),
      'stacktrace': traceback.format_exc().splitlines()
    }

fetch = Tool(
  name="fetch",
  description="Execute a fetch method",
  func=exec_fetch
)