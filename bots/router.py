import sys
import os
import json
from bots.utils.prompts import instructions_and_request
from bots.utils.llms import call_llm
# Casts functions
from bots.actions.digest_casts import DigestCasts
from bots.actions.pick_cast import PickCast
# User functions
from bots.actions.favorite_users import FavoriteUsers
from bots.actions.most_active_users import MostActiveUsers
from bots.actions.prefs_cloud import PrefsCloud
from bots.actions.psycho import Psycho
from bots.actions.roast import Roast
# Generic functions
from bots.actions.run_sql import RunSql


def read_functions_md():
  current_dir = os.path.dirname(os.path.abspath(__file__))
  functions_path = os.path.join(current_dir, '..', 'functions.md')
  with open(functions_path, 'r') as file:
    functions = file.read()
  return functions

intro = """
INSTRUCTIONS:
Map the query to one of the following actions.
Your goal is not to answer the query.
Just find the function that should be used to reply to the query.
"""

functions = read_functions_md()

format = """
RESPONSE FORMAT:
{
  "function": function_number_from_the_provided_list
}
"""

instructions = intro + '\n' + functions + '\n' + format

actions ={
  10: DigestCasts,
  11: PickCast,

  21: FavoriteUsers,
  22: MostActiveUsers,
  23: PrefsCloud, 
  24: Psycho,
  25: Roast,

  91: RunSql,
  92: None
}

def find_action(request):
  prompt = instructions_and_request(instructions, request)
  result = call_llm(prompt)
  return result

def route(request, fid_origin=None):
  print('request', request)
  mapped = find_action(request)
  print('mapped', mapped)  
  if ('function' not in mapped or mapped['function'] not in actions):
    raise Exception('Could not map the request to a bot action.')
  function_number = int(mapped['function'])
  Action = actions[function_number]
  action = Action()
  action.parse(request, fid_origin)
  return action


if __name__ == "__main__":
  request = sys.argv[1]
  action = route(request)
  print(action)
  action.get_cost()
  print(f"Cost: {action.cost}")
  action.execute()
  print(f"Data: {action.data}")
  action.get_casts()
  print(f"Casts: {action.casts}")