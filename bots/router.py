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
Do not pick the roast or psychoanalyze actions unless the user clearly asks for it in the last post of the conversation, if not sure, avoid the Roast and Psycho actions.
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
  username_origin = get_username(fid_origin) if fid_origin is not None else 'unknown_user'
  main_cast = {'text': request, 'fid': fid_origin, 'username': username_origin}
  if attachment_hash is not None:
    attachment_cast = get_cast(attachment_hash)
    main_cast['quote'] = {'text': attachment_cast['text'], 'fid': attachment_cast['fid'], 'username': attachment_cast['username']}
  context.append(main_cast)
  max_depth = 7
  current_depth = 0
  while parent_hash is not None and current_depth < max_depth:
    previous_cast = get_cast(parent_hash)
    context.append(previous_cast)
    parent_hash = previous_cast['parent_hash']
    current_depth += 1
  context.reverse()
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
    text += f"#{i+1}. @{item['username']} said: \n"
    text += f"{item['text']} \n"  
    if 'quote' in item:
      text += f"  [quoting @{item['quote']['username']}: \n"
      text += f"  {item['quote']['text']} \n"
      text += "  ]\n"
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