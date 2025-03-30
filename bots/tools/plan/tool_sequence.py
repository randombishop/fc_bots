from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.helpers import HELPERS_TOOLS

tool_list = PARSE_TOOLS + FETCH_TOOLS + PREPARE_TOOLS + HELPERS_TOOLS

tool_map = {x.name: x for x in tool_list} 

providers_map = {}
for t in tool_list:
  for o in t.metadata['outputs']:
    if o not in providers_map:
      providers_map[o] = []
    providers_map[o].append(t.name)

def get_missing_inputs(tool_name, available_data, inputs):
  tool = tool_map[tool_name]
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
  
def are_all_outputs_already_set(tool_name, available_data):
  tool = tool_map[tool_name]
  return all(x in available_data for x in tool.metadata['outputs'])

def are_all_inputs_already_set(tool_name, available_data):
  missing_inputs, _ = get_missing_inputs(tool_name, available_data, [])
  return len(missing_inputs) == 0
  
def add_tool_to_chain(tool_name, tool_chain, available_data):
  print(f'add_tool_to_chain: {tool_name}, tool_chain={tool_chain}')
  tool = tool_map[tool_name]
  for output in tool.metadata['outputs']:
    available_data[output] = True
  tool_chain.append(tool_name)

def choose_provider(providers):
  raise Exception(f'choose_provider not implemented yet. providers={",".join(providers)}')

def compile_tool(tool_name, tool_chain, available_data):
  print(f'compile_tool: {tool_name}, current_tool_chain={tool_chain}')
  if are_all_outputs_already_set(tool_name, available_data):
    print(f'skipping {tool_name} because all outputs are already set')
    return
  if are_all_inputs_already_set(tool_name, available_data):
    print(f'adding {tool_name} to tool_chain because all inputs are already set')
    add_tool_to_chain(tool_name, tool_chain, available_data)
    return
  missing_inputs, require = get_missing_inputs(tool_name, available_data, [])
  print(f'missing_inputs={missing_inputs}, require={require}')
  if require == 'all':
    for missing_input in missing_inputs:
      if missing_input not in providers_map:
        raise Exception(f"No provider found for {missing_input}")
    providers = providers_map[missing_input]
    if len(providers) == 1:
      compile_tool(providers[0], tool_chain, available_data)
    else:
      provider = choose_provider(providers)
      compile_tool(provider, tool_chain, available_data)
  elif require == 'any':
    candidates = []
    for missing_input in missing_inputs:
      if missing_input in providers_map:
        candidates.extend(providers_map[missing_input])
    candidates = list(set(candidates))
    if len(candidates) == 0:
      raise Exception(f"No provider found to satisfy any[{','.join(missing_inputs)}]")
    elif len(candidates) == 1:
      compile_tool(candidates[0], tool_chain, available_data)
    else:
      provider = choose_provider(candidates)
      compile_tool(provider, tool_chain, available_data)
  add_tool_to_chain(tool_name, tool_chain, available_data)

def compile_sequence(tool_names, available_data):
  print('-'*100)
  print('Compiling sequence...')
  tool_names = tool_names.split(',') if tool_names is not None else []
  tool_names = [x.strip() for x in tool_names]
  tool_names = [x for x in tool_names if x in tool_map]
  print(f'tool_names={tool_names}')
  simulated_data = {x:True for x in available_data.keys()}
  print(f'simulated_data={simulated_data}')
  tool_chain = []
  for t in tool_names:
    compile_tool(t, tool_chain, simulated_data)
  print(f'tool_chain={tool_chain}')
  print('-'*100)
  return tool_chain

def get_tool(tool_name):
  return tool_map[tool_name]