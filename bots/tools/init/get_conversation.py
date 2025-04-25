from langchain.agents import Tool
from bots.data.neynar import get_cast_info
from bots.data.users import get_username


max_depth = 28


def get_conversation(input):
  state = input.state
  context = []
  fid_origin = state.get('fid_origin')
  username_origin = get_username(fid_origin) if fid_origin is not None else 'unknown_user'
  request = state.get('request')
  attachment_hash = state.get('attachment_hash')
  if request is not None or attachment_hash is not None:
    main_cast = {
      'text': request if request is not None else '', 
      'fid': fid_origin, 
      'username': username_origin, 
      'when': 'now'
    }
    if attachment_hash is not None:
      attachment_cast = get_cast_info(attachment_hash)
      if attachment_cast is not None:
        main_cast['quote'] = {'text': attachment_cast['text'], 'fid': attachment_cast['fid'], 'username': attachment_cast['username']}
    context.append(main_cast)
  current_depth = 0
  parent_hash = state.get('parent_hash')
  while parent_hash is not None and current_depth < max_depth:
    previous_cast = None
    try:
      previous_cast = get_cast_info(parent_hash)
    except:
      pass
    if previous_cast is not None:
      context.append(previous_cast)
      parent_hash = previous_cast['parent_hash']
      current_depth += 1
    else:
      parent_hash = None
  context.reverse()
  text = ''
  for i in range(len(context)):
    item = context[i]
    text += f"#{i+1}. @{item['username']} said {item['when']}: \n"
    text += f"{item['text']} \n"  
    if 'quote' in item:
      if 'username' in item['quote']:
        text += f"  [quoting @{item['quote']['username']}: \n"
        text += f"  {item['quote']['text']} \n"
        text += "  ]\n"
      elif 'url' in item['quote']:
        text += f"  [{item['quote']['url']}]\n"
    text += '#'
  return {'conversation': text}


GetConversation = Tool(
  name="GetConversation",
  func=get_conversation,
  description="Get the current conversation"
)