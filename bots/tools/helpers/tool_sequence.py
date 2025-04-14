from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.helpers import HELPERS_TOOLS
from bots.tools.helpers.pick_provider import pick_provider
from bots.tools.helpers.tool_io import missing_inputs, all_outputs_already_set


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
  return missing_inputs(tool, available_data, inputs)
  
def are_all_outputs_already_set(tool_name, available_data):
  tool = tool_map[tool_name]
  return all_outputs_already_set(tool, available_data)

def are_all_inputs_already_set(tool_name, available_data):
  missing_inputs, _ = get_missing_inputs(tool_name, available_data, [])
  return len(missing_inputs) == 0
  
def add_tool_to_chain(tool_name, tool_chain, available_data):
  tool = tool_map[tool_name]
  for output in tool.metadata['outputs']:
    available_data[output] = True
  tool_chain.append(tool_name)

def choose_provider(tool_name, provider_names, state, log):
  log.append(f'Choosing provider for {tool_name}: {provider_names}')
  tool = tool_map[tool_name]
  providers = [tool_map[x] for x in provider_names]
  provider = pick_provider(tool, providers, state)
  if provider is None or provider not in provider_names:
    raise Exception(f"Could not select a provider for {tool_name}.  Available providers: {provider_names}. Selected provider: {provider}")
  log.append(f'Selected provider: {provider}')
  return provider

def compile_tool(tool_name, tool_chain, available_data, state, log):
  log.append(f'Compiling tool: {tool_name}')
  if are_all_outputs_already_set(tool_name, available_data):
    log.append(f'Skipping {tool_name} because all outputs are already set')
    return
  if are_all_inputs_already_set(tool_name, available_data):
    log.append(f'Adding {tool_name} to tool_chain because all inputs are already set')
    add_tool_to_chain(tool_name, tool_chain, available_data)
    log.append(f'Tool chain: {tool_chain}')
    return
  missing_inputs, require = get_missing_inputs(tool_name, available_data, [])
  log.append(f'missing_inputs={missing_inputs}, require={require}')
  if require == 'all':
    for missing_input in missing_inputs:
      if missing_input not in providers_map:
        raise Exception(f"No provider found for {missing_input}")
      providers = providers_map[missing_input]
      log.append(f'{missing_input} <-- {providers}')
      if len(providers) == 1:
        compile_tool(providers[0], tool_chain, available_data, state, log)
      else:
        provider = choose_provider(tool_name, providers, state, log)
        compile_tool(provider, tool_chain, available_data, state, log)
  elif require == 'any':
    candidates = []
    for missing_input in missing_inputs:
      if missing_input in providers_map:
        candidates.extend(providers_map[missing_input])
    candidates = list(set(candidates))
    log.append(f'{missing_inputs} <-- {candidates}')
    if len(candidates) == 0:
      raise Exception(f"No provider found to satisfy any[{','.join(missing_inputs)}]")
    elif len(candidates) == 1:
      compile_tool(candidates[0], tool_chain, available_data, state, log)
    else:
      provider = choose_provider(tool_name, candidates, state, log)
      compile_tool(provider, tool_chain, available_data, state, log)
  log.append(f'Adding {tool_name} to tool_chain after compiling its dependencies')
  add_tool_to_chain(tool_name, tool_chain, available_data)
  log.append(f'Tool chain: {tool_chain}')

def clean_tools(tool_names, valid_names):
  if isinstance(tool_names, str):
    tool_names = tool_names.split(',') if tool_names is not None else []
  elif isinstance(tool_names, list):
    tool_names = tool_names
  else:
    return []
  tool_names = [x.strip() for x in tool_names]
  tool_names = [x for x in tool_names if x in valid_names]
  return tool_names

def compile_sequence(state, tool_names):
  log = []
  available_data = state.get_available_data()
  log.append(f'Compiling sequence: {tool_names}')
  simulated_data = {x:True for x in available_data.keys()}
  log.append(f'Simulated data: {simulated_data}')
  tool_chain = []
  for t in tool_names:
    compile_tool(t, tool_chain, simulated_data, state, log)
  log.append(f'Tool chain fully compiled: {tool_chain}')
  return tool_chain, log

def get_tool(tool_name):
  return tool_map[tool_name]

def format_tool(tool):
  return f"##{tool.name}\n{tool.description}\n"

def filter_suggested_tools(tool_names, available_data):
  ans = []
  for t in tool_names:
    inputs_ready = are_all_inputs_already_set(t, available_data)
    outputs_already_set = are_all_outputs_already_set(t, available_data)
    if inputs_ready and not outputs_already_set:
      ans.append(t)
  return ans