from langchain.agents import Tool
from bots.data.app import get_bot_character
from bots.utils.llms import get_max_capactity
from bots.data.users import get_username, get_fid
from bots.data.channels import get_channel_url


def initialize_tools(mode):
  if mode == 'assistant':
    return ['GetBio', 'GetLore', 'GetStyle', 'GetTime']
  elif mode == 'bot':
    return ['GetBio', 'GetLore', 'GetStyle', 'GetTime', 'GetConversation']
  elif mode == 'blueprint':
    return ['GetBio', 'GetLore', 'GetStyle', 'GetTime']
  else:
    raise Exception(f"Agent mode {mode} not found")

def init_state(input):    
  id = input['bot_id']
  character = get_bot_character(id)
  mode = input['mode']
  if mode not in ['assistant', 'bot', 'blueprint']:
    raise Exception(f"Invalid mode `{mode}`. should be assistant, bot or blueprint")
  if character is None:
    raise Exception(f"Bot {id} not found")
  input['state'].character = character
  ans = {}
  ans['id'] = id
  ans['name'] = character['name']
  ans['mode'] = mode
  if 'request' in input and input['request'] is not None:
    ans['request'] = input['request']
  if 'fid_origin' in input and input['fid_origin'] is not None:
    ans['fid_origin'] = int(input['fid_origin'])
    ans['user_origin'] = get_username(ans['fid_origin'])
  if 'parent_hash' in input and input['parent_hash'] is not None:
    ans['parent_hash'] = input['parent_hash']
  if 'attachment_hash' in input and input['attachment_hash'] is not None:
    ans['attachment_hash'] = input['attachment_hash']
  if 'root_parent_url' in input and input['root_parent_url'] is not None:
    ans['root_parent_url'] = input['root_parent_url']
  if 'user' in input and input['user'] is not None:
    ans['user'] = input['user']
    ans['user_fid'] = get_fid(ans['user'])
  if 'channel' in input and input['channel'] is not None:
    ans['channel'] = input['channel']
    ans['channel_url'] = get_channel_url(ans['channel'])
  if 'blueprint' in input and input['blueprint'] is not None:
    ans['blueprint'] = input['blueprint']
  ans['should_continue'] = True
  ans['max_rows'] = get_max_capactity()
  ans['todo'] = initialize_tools(mode)
  return ans
  

InitState = Tool(
  name="InitState",
  func=init_state,
  description="Initialize the state of the bot."
)