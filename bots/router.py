import sys
from bots.utils.llms import call_llm
from bots.catalog import ACTIONS, DESCRIPTIONS
from bots.data.casts import get_cast
from bots.data.users import get_username
from bots.data.channels import get_channel_by_url
from bots.action.like import Like


# Main task prompt
# ----------------



def find_action(request):
  instructions = main_task + '\n' 
  instructions += 'LIST OF ACTIONS:\n'
  instructions += DESCRIPTIONS + '\n'
  instructions += 'OUTPUT FORMAT:\n'
  instructions += main_format
  result = call_llm(request,instructions, main_schema)
  return result







def route(request, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None):
  context = get_context(request, fid_origin, parent_hash, attachment_hash)
  context = format_context(context, root_parent_url)
  mapped = find_action(request)
  Action = None
  if ('action' not in mapped or mapped['action'] is None or str(mapped['action']) not in ACTIONS):
    Action = Like
  else:
    f = str(mapped['action'])
    Action = ACTIONS[f]
  action = Action()
  action.set_fid_origin(fid_origin)
  action.set_root_parent_url(root_parent_url)
  action.set_input(context)
  return action

