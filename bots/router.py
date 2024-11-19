import sys
import os
import json
from bots.utils.prompts import instructions_and_request
from bots.utils.llms import call_llm
from bots.catalog import ACTIONS, DESCRIPTIONS





intro = """
INSTRUCTIONS:
Map the query to one of the following actions.
Your goal is not to answer the query.
Just find the action that matches the user intent.
"""

format = """
RESPONSE FORMAT:
{
  "function": one of [?]}
}
""".replace('?', ','.join([str(x) for x in ACTIONS.keys()]))

instructions = intro + '\n' + DESCRIPTIONS + '\n' + format



def find_action(request):
  prompt = instructions_and_request(instructions, request)
  result = call_llm(prompt)
  return result

def route(request, fid_origin=None, parent_hash=None, attachment_hash=None):
  mapped = find_action(request)
  if ('function' not in mapped or mapped['function'] not in ACTIONS):
    raise Exception('Could not map the request to a bot action.')
  function_number = int(mapped['function'])
  Action = ACTIONS[function_number]
  action = Action()
  action.set_fid_origin(fid_origin)
  action.set_parent_hash(parent_hash)
  action.set_attachment_hash(attachment_hash)
  action.set_input(request)
  return action


if __name__ == "__main__":
  request = sys.argv[1]
  fid_origin = sys.argv[2] if len(sys.argv) > 2 else None
  parent_hash = sys.argv[3] if len(sys.argv) > 3 else None
  action = route(request, fid_origin=fid_origin, parent_hash=parent_hash)
  print(action)
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.get_data()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")