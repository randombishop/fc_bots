from langchain.agents import Tool
from bots.data.casts import get_cast
from bots.data.users import get_username


max_depth = 28


def get_conversation(state):
  context = []
  username_origin = get_username(state.fid_origin) if state.fid_origin is not None else 'unknown_user'
  if state.request is not None or state.attachment_hash is not None:
    main_cast = {
      'text': state.request if state.request is not None else '', 
      'fid': state.fid_origin, 
      'username': username_origin, 
      'when': 'now'
    }
    if state.attachment_hash is not None:
      attachment_cast = get_cast(state.attachment_hash)
      if attachment_cast is not None:
        main_cast['quote'] = {'text': attachment_cast['text'], 'fid': attachment_cast['fid'], 'username': attachment_cast['username']}
    context.append(main_cast)
  current_depth = 0
  parent_hash = state.parent_hash
  while parent_hash is not None and current_depth < max_depth:
    previous_cast = get_cast(parent_hash)
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
      text += f"  [quoting @{item['quote']['username']}: \n"
      text += f"  {item['quote']['text']} \n"
      text += "  ]\n"
    text += '#'
  state.conversation = text
  return {'conversation': state.conversation}


GetConversation = Tool(
  name="get_conversation",
  func=get_conversation,
  description="Get the current conversation"
)