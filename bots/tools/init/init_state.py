from langchain.agents import Tool
from bots.data.app import get_bot_character
from bots.utils.llms import get_max_capactity
from bots.data.users import get_username, get_fid
from bots.data.channels import get_channel_url


def init_state(input):    
  id = input['bot_id']
  character = get_bot_character(id)
  if character is None:
    raise Exception(f"Bot {id} not found")
  request = input['request'] if 'request' in input else None
  fid_origin = int(input['fid_origin']) if 'fid_origin' in input and input['fid_origin'] is not None else None
  user_origin = get_username(fid_origin) if fid_origin is not None else None
  parent_hash = input['parent_hash'] if 'parent_hash' in input else None
  attachment_hash = input['attachment_hash'] if 'attachment_hash' in input else None
  root_parent_url = input['root_parent_url'] if 'root_parent_url' in input else None
  user = input['user'] if 'user' in input else None
  user_fid = get_fid(user) if user is not None else None
  channel = input['channel'] if 'channel' in input else None
  channel_url = get_channel_url(channel) if channel is not None else None
  return {
    'id': id,
    'name': character['name'],
    'character': character,
    'request': request,
    'fid_origin': fid_origin,
    'user_origin': user_origin,
    'parent_hash': parent_hash,
    'attachment_hash': attachment_hash,
    'root_parent_url': root_parent_url,
    'user': user,
    'user_fid': user_fid,
    'channel': channel,
    'channel_url': channel_url,
    'keyword': None,
    'category': None,
    'search': None,
    'text': None,
    'question': None,
    'criteria': None,
    'max_rows': get_max_capactity()
  }
  
InitState = Tool(
  name="InitState",
  func=init_state,
  description="Initialize the state of the bot."
)