from bots.i_wakeup_step import IWakeUpStep
from bots.data.casts import get_cast
from bots.data.users import get_username


class WakeUpConversation(IWakeUpStep):
    
  def get(self, bot_character, bot_state):
    context = []
    username_origin = get_username(bot_state.fid_origin) if bot_state.fid_origin is not None else 'unknown_user'
    main_cast = {'text': bot_state.request, 'fid': bot_state.fid_origin, 'username': username_origin}
    if bot_state.attachment_hash is not None:
      attachment_cast = get_cast(bot_state.attachment_hash)
      if attachment_cast is not None:
        main_cast['quote'] = {'text': attachment_cast['text'], 'fid': attachment_cast['fid'], 'username': attachment_cast['username']}
    context.append(main_cast)
    max_depth = 7
    current_depth = 0
    parent_hash = bot_state.parent_hash
    while parent_hash is not None and current_depth < max_depth:
      previous_cast = get_cast(bot_state.parent_hash)
      if previous_cast is not None:
        context.append(previous_cast)
        bot_state.parent_hash = previous_cast['parent_hash']
        current_depth += 1
      else:
        parent_hash = None
    context.reverse()
    text = ''
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
