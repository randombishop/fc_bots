from dotenv import load_dotenv
load_dotenv()
import sys
from bots.utils.llms import call_llm
from bots.catalog import ACTIONS, DESCRIPTIONS
from bots.data.casts import get_cast
from bots.data.users import get_username
from bots.data.channels import get_channel_by_url
from bots.actions.like import Like


# Main task prompt
# ----------------

main_task = """
You are a social media bot programmed to perform a specific set of actions.

INSTRUCTIONS:
Map the query to one of the following actions.
Your goal is not to answer the query, you must only decide which action to perform.
Decide the action that matches the user intent.
Pick one specific action based on the conversation if it is relevant and useful for the user, but if no specific action is applicable, return an error message and a null action.
"""

main_format = """
{
  "action": "..."
}
"""

main_schema = {
  "type":"OBJECT",
  "properties":{
    "action":{"type":"STRING"}, 
    "error":{"type":"STRING"}
  }
}

def find_action(request):
  instructions = main_task + '\n' 
  instructions += 'LIST OF ACTIONS:\n'
  instructions += DESCRIPTIONS + '\n'
  instructions += 'OUTPUT FORMAT:\n'
  instructions += main_format
  result = call_llm(request,instructions, main_schema)
  return result







# Bot Logic
# ----------------

def get_context(request, fid_origin=None, parent_hash=None, attachment_hash=None):
  context = []
  context.append({'text': '@dsart ' + request, 'fid': fid_origin})
  max_depth = 7
  current_depth = 0
  while parent_hash is not None and current_depth < max_depth:
    cast = get_cast(parent_hash)
    context.append({'text': cast['text'], 'fid': cast['fid']})
    parent_hash = cast['parent_hash']
    current_depth += 1
  context.reverse()
  fids = list(set(item['fid'] for item in context if item['fid'] is not None))
  fids = [x for x in fids if x is not None]
  usernames = {}
  if len(fids) > 0:
    for fid in fids:
      usernames[fid] = get_username(fid)
  for item in context:
    if item['fid'] is None:
      item['username'] = '@unknown_user'
    elif item['fid'] in usernames:
      item['username'] = '@' +usernames[item['fid']]
    elif item['fid'] is not None:
      item['username'] = '@fid#' + str(item['fid'])
  return context
 
def format_context(context, root_parent_url=None):
  text = ''
  if root_parent_url is not None:
    channel_id = get_channel_by_url(root_parent_url)
    if channel_id is not None:
      text += '#CURRENT CHANNEL: /'+channel_id+'\n'
  text += "#CONVERSATION:\n"
  for i in range(len(context)):
    item = context[i]
    text += f"#{i+1}. {item['username']} said: "
    text += f"{item['text']} \n"  
    text += '#\n'
  return text

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
  action.set_parent_hash(parent_hash)
  action.set_attachment_hash(attachment_hash)
  action.set_root_parent_url(root_parent_url)
  action.set_input(context)
  return action


if __name__ == "__main__":
  request = sys.argv[1]
  fid_origin = sys.argv[2] if len(sys.argv) > 2 else None
  parent_hash = sys.argv[3] if len(sys.argv) > 3 else None
  action = route(request, fid_origin=fid_origin, parent_hash=parent_hash)
  action.run()
  action.print()