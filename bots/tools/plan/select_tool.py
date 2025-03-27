from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS


select_tool_task = """
#TASK
You are @{{name}}, a social media bot with access to a set of tools.
Given the provided context and instructions, which tool should you run next?
You must only decide which tool to execute next.
The tools use parameters from the current context so make sure their parameters are set before calling them.
If you are done running tools and don't need to run a new one, respond with {"tool": null, "ready": true}
If you can't figure out how to respond and none of tools would help further, respond with {"tool": null, "ready": false}
If running a tool will be helpful to improve the quality of your response, respond with {"tool": "...", "ready": false}
Also provide a reasoning for your choice.

#AVAILABLE TOOLS
available_tools?

#OUTPUT FORMAT
{
  "tool": "...",
  "ready": true|false,
  "reasoning": "..."
}
"""

select_tool_schema = {
  "type":"OBJECT",
  "properties":{
    "tool":{"type":"STRING"},
    "ready":{"type":"BOOLEAN"},
    "reasoning":{"type":"STRING"}
  }
}

tool_names = [x.name for x in PARSE_TOOLS + FETCH_TOOLS + PREPARE_TOOLS]

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

def is_tool_available(tool, available_data):
  metadata = tool.metadata
  if metadata is None:
    return True
  inputs = metadata['inputs'] if 'inputs' in metadata else []
  require_inputs = metadata['require_inputs'] if 'require_inputs' in metadata else 'all'
  inputs_ok =  check_inputs(available_data, inputs, require_inputs)
  if not inputs_ok:
    return False
  outputs = metadata['outputs'] if 'outputs' in metadata else []
  outputs_ok = check_outputs(available_data, outputs)
  return outputs_ok

def filterTools(list, available_data):
  return [x for x in list if is_tool_available(x, available_data)]

def format_tools(list):
  ans = ''
  for x in list:
    ans += f"{x.name}: {x.description}\n"
  return ans

def get_available_tools(available_data):
  ans = ''
  num_tools = 0
  parse = filterTools(PARSE_TOOLS, available_data)
  if len(parse) > 0:
    ans += f"## For setting parameters\n{format_tools(parse)}\n"
    num_tools += len(parse)
  fetch = filterTools(FETCH_TOOLS, available_data)
  if len(fetch) > 0:
    ans += f"## For fetching your data\n{format_tools(fetch)}\n"
    num_tools += len(fetch)
  prepare = filterTools(PREPARE_TOOLS, available_data)
  if len(prepare) > 0:
    ans += f"## To prepare additional data before posting (such as charts, images, summaries, wordclouds, etc.)\n{format_tools(prepare)}\n"
    num_tools += len(prepare)
  return ans, num_tools

def select_tool(input):
  state = input.state
  llm = input.llm
  available_data = state.get_available_data()
  available_tools, num_tools = get_available_tools(available_data)
  if num_tools == 0:
    return {
      'next_tool': None,
      'tools_done': True,
      'next_tool_reasoning': 'No tools available'
    }
  request = state.get('request')
  if request is None or len(request) == 0:
    raise Exception('No request provided')
  prompt = state.format_tools_log()
  instructions = state.format(select_tool_task)
  instructions = instructions.replace('available_tools?', available_tools)
  result = call_llm(llm, prompt, instructions, select_tool_schema)
  next_tool = result['tool']
  tools_done = result['ready']
  if next_tool not in tool_names:
    next_tool = None
    tools_done = True
  state.next_tool = next_tool
  state.tools_done = tools_done
  reasoning = result['reasoning'] if 'reasoning' in result else ''
  return {
    'next_tool': state.next_tool, 
    'tools_done': state.tools_done,
    'next_tool_reasoning': reasoning
  }
  

SelectTool = Tool(
  name="SelectTool",
  func=select_tool,
  description="Select the next tool to run"
)
