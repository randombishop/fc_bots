

def missing_inputs(tool, available_data, inputs):
  metadata = tool.metadata
  if metadata is None:
    return [], None
  inputs = metadata['inputs'] if 'inputs' in metadata else []
  require = metadata['require_inputs'] if 'require_inputs' in metadata else 'all'
  if require not in ['all', 'any']:
    raise Exception('require_inputs must be "all" or "any"')
  if len(inputs) == 0:
    return [], None
  elif require == 'all':
    if all(x in available_data for x in inputs):
      return [], None
    else:
      return [x for x in inputs if x not in available_data], 'all'
  elif require == 'any':
    if any(x in available_data for x in inputs):
      return [], None
    else:
      return inputs, 'any'

    
def all_outputs_already_set(tool, available_data):
  return all(x in available_data for x in tool.metadata['outputs'])