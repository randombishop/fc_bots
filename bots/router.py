from dotenv import load_dotenv
load_dotenv()
import sys
from bots.utils.llms import call_llm
from bots.catalog import ACTIONS, DESCRIPTIONS


task = """
Map the query to one of the following actions.
Your goal is not to answer the query.
Just find the action that matches the user intent.
Try to map the query to one of the specific actions as much as possible, only when no specific action is found, map to the general action "Chat".
"""

format = """
{
  "function": "..."
}
"""


def find_action(request):
  instructions = task + '\n' 
  instructions += 'LIST OF ACTIONS:\n'
  instructions += DESCRIPTIONS + '\n'
  instructions += 'OUTPUT FORMAT:\n'
  instructions += format
  schema = {
    "type":"OBJECT",
    "properties":{
      "function":{"type":"STRING"}, 
      "error":{"type":"STRING"}
    }
  }
  result = call_llm(request,instructions, schema)
  return result


def route(request, fid_origin=None, parent_hash=None, attachment_hash=None):
  mapped = find_action(request)
  if ('function' not in mapped or str(mapped['function']) not in ACTIONS):
    message = 'Could not map the request to a bot action.'
    message += f"\nRequest: {request}"
    message += f"\nMapped: {mapped}"
    raise Exception(message)
  f = str(mapped['function'])
  Action = ACTIONS[f]
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
  action.run()
  action.print()