from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS


tool_map = {x.name: x for x in PARSE_TOOLS + FETCH_TOOLS + PREPARE_TOOLS} 


def add_dependecies(tool_name, available_data):
  return [tool_name]

def validate_sequence(tool_names, available_data):
  tool_names = tool_names.split(',') if tool_names is not None else None
  tool_names = [x.strip() for x in tool_names]
  tool_names = [x for x in tool_names if x in tool_map]
  simulated_data = {x:True for x in available_data.keys()}
  validated = []
  for t in tool_names:
    tool = tool_map[t]
    already_set = all(x in available_data for x in tool.metadata['outputs'])
    if not already_set:
      chain = add_dependecies(t, available_data)
      for c in chain:
        for d in c.metadata['outputs']:
          simulated_data[d] = True
      validated = validated + chain
  return validated