from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS


select_tool_task = """
#TASK
You are @{{name}}, a social media bot with access to a set of tools.
Given the provided context and instructions, which tool sequence should you run next?
You must only decide which tools to execute next.
If you are done running tools and don't need to run a new one, respond with {"tools": null}
If you can't figure out how to respond and none of the tools would help further, respond with {"tools": null}
If running a tool or more will be helpful to improve the quality of your response, respond with {"tools": "..."}
Your tool sequence should start with one of the tools for which parameters are already set.
Study the inputs/outputs of tools carefully to make sure each tool in the sequence will have its parameters ready when called.


#OUTPUT FORMAT
{
  "tools": "comma separated list of tools to execute next"
}

"""

select_tool_schema = {
  "type":"OBJECT",
  "properties":{
    "tools":{"type":"STRING"}
  }
}

tool_map = {x.name: x for x in PARSE_TOOLS + FETCH_TOOLS + PREPARE_TOOLS}

def check_inputs(available_data, inputs, require_inputs):
  if require_inputs not in ['all', 'any']:
    raise Exception('require_inputs must be "all" or "any"')
  if len(inputs) == 0:
    return True
  elif require_inputs == 'all':
    return all(x in available_data for x in inputs)
  elif require_inputs == 'any':
    return any(x in available_data for x in inputs)

def check_outputs(available_data, outputs):
  if len(outputs) == 0:
    return True
  else:
    return all(x not in available_data for x in outputs)

def are_inputs_ready_for_tool(tool, available_data):
  metadata = tool.metadata
  if metadata is None:
    return True
  inputs = metadata['inputs'] if 'inputs' in metadata else []
  require_inputs = metadata['require_inputs'] if 'require_inputs' in metadata else 'all'
  return check_inputs(available_data, inputs, require_inputs)
  
def are_tool_outputs_already_set(tool, available_data):
  metadata = tool.metadata
  if metadata is None:
    return False
  outputs = metadata['outputs'] if 'outputs' in metadata else []
  return not check_outputs(available_data, outputs)

def is_tool_available(tool, available_data):
  inputs_ok = are_inputs_ready_for_tool(tool, available_data)
  outputs_ok = not are_tool_outputs_already_set(tool, available_data)
  return inputs_ok and outputs_ok

def filterTools(list, available_data):
  return [x for x in list if is_tool_available(x, available_data)]

def format_tool(tool, available_data):
  metadata = tool.metadata
  ans = f"###{tool.name}\n"
  ans += f"Description: {tool.description}\n"
  ans += 'Inputs: '
  if metadata is not None and 'inputs' in metadata:
    require_inputs = metadata['require_inputs'] if 'require_inputs' in metadata else 'all'
    ans += f"Requires {require_inputs} of ["
    ans += ', '.join(metadata['inputs'])
    ans += ']'
    if are_inputs_ready_for_tool(tool, available_data):
      ans += ' (ready)'
    else:
      if require_inputs == 'all':
        missing_params = ', '.join([x for x in metadata['inputs'] if x not in available_data])
        ans += f' (Missing parameters: {missing_params}. Make sure these will be set before in the tools sequence.)'
      else:
        ans += ' (Make sure at least one of the parameters will be set before in the tools sequence.)'
    ans += '\n'
  else:
    ans += '[]\n'
  ans += 'Outputs: ['
  if metadata is not None and 'outputs' in metadata:
    ans += ', '.join(metadata['outputs'])
    ans += ']'
    if are_tool_outputs_already_set(tool, available_data):
      ans += ' (outputs were already set, avoid re-running unless parameters changed.)'
    ans += '\n'
  return ans
  
def format_tools(list, available_data):
  ans = ''
  for x in list:
    formatted = format_tool(x, available_data)
    ans += (formatted +"\n")
  return ans

def get_available_tools(available_data):
  tool_list = []
  parse = filterTools(PARSE_TOOLS, available_data)
  tool_list.extend([x.name for x in parse])
  fetch = filterTools(FETCH_TOOLS, available_data)
  tool_list.extend([x.name for x in fetch])
  prepare = filterTools(PREPARE_TOOLS, available_data)
  tool_list.extend([x.name for x in prepare])
  return tool_list

def format_tools_prompt(state, available_tools, available_data):
  ans = '#TOOLS ALREADY EXECUTED:\n'
  for x in state.tools_log:
    step = x[0]
    if step.tool not in ['InitState', 'AssistantWakeup', 'BotWakeup', 'SelectTool']:
      observation = x[1]
      outputs = ', '.join(observation.keys())
      ans += f"{step.tool} -> [{outputs}]\n"
  ans += '\n'
  ans += '#CURRENTLY AVAILABLE PARAMETERS:\n'
  ans += ','.join(state.get_available_data().keys())
  ans += '\n\n'
  ans += '#YOUR TOOL BOX:\n\n'
  ans += '##For setting parameters\n\n'
  ans += format_tools(PARSE_TOOLS, available_data)
  ans += '##For fetching your data\n\n'
  ans += format_tools(FETCH_TOOLS, available_data)
  ans += '##To prepare additional data before posting (such as charts, images, summaries, wordclouds, etc.)\n'
  ans += f"You are encouraged to try these as much as possible to enrich your context and improve your response:\n"
  ans += format_tools(PREPARE_TOOLS, available_data)
  ans += '\n\n'
  ans += "#CURRENTLY READY-TO-USE TOOLS (Your sequence must start with one of these)\n"
  ans += ', '.join(available_tools)
  ans += '\n\n'
  ans += '#YOUR INSTRUCTIONS\n'
  ans += state.get('request')
  return ans

def validate_sequence(tools, available_data):
  tools = [x.strip() for x in tools]
  tools = [x for x in tools if x in tool_map]
  simulated_data = {x:True for x in available_data.keys()}
  validated = []
  ok = True
  i = 0
  while ok and i < len(tools):
    t = tools[i]
    tool = tool_map[t]
    valid = are_inputs_ready_for_tool(tool, simulated_data)
    valid = valid and (not are_tool_outputs_already_set(tool, simulated_data))
    if valid:
      i += 1
      validated.append(t)
      for output in tool.metadata['outputs']:
        simulated_data[output] = True
    else:
      ok = False
  return validated

def select_tool(input):
  state = input.state
  llm = input.llm
  available_data = state.get_available_data()
  available_tools = get_available_tools(available_data)
  if len(available_tools) == 0:
    state.prepared = True
    return {
      'next_tools': None,
      'next_tools_llm': 'Skipped because no tools available'
    }
  prompt = format_tools_prompt(state, available_tools, available_data)
  instructions = state.format(select_tool_task)
  result = call_llm(llm, prompt, instructions, select_tool_schema)
  next_tools_llm = result['tools'] if 'tools' in result else None
  next_tools = next_tools_llm.split(',') if next_tools_llm is not None else None
  next_tools = validate_sequence(next_tools, available_data)
  if next_tools is None or len(next_tools) == 0:
    state.prepared = True
  return {
    'next_tools': next_tools,
    'next_tools_llm': next_tools_llm
  }
  
  
SelectTool = Tool(
  name="SelectTool",
  func=select_tool,
  description="Select the next tool to run"
)
