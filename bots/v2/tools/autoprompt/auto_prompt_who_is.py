from langchain.agents import Tool
from bots.data.bot_history import get_random_user_to_praise, get_random_user_to_praise_in_channel
from bots.data.users import get_fid
from bots.data.channels import get_channel_url


def auto_prompt_who_is(input):
  state = input['state']
  user_name, fid = None, None
  channel_url = get_channel_url(state.selected_channel)
  if state.user is not None:
    user_name = state.user
    fid = get_fid(user_name)
  elif channel_url is None:
    user_name = get_random_user_to_praise(state.id)
    fid = get_fid(user_name)
  else:
    user_name = get_random_user_to_praise_in_channel(state.id, channel_url)
    fid = get_fid(user_name)
  state.request = f'Who is {user_name}?'  
  state.action_params = {'fid': fid, 'user_name': user_name}
  state.user_fid = fid
  state.user = user_name
  state.conversation = state.request
  return {
    'action_params': state.action_params,
    'user_fid': state.user_fid,
    'user': state.user,
    'request': state.request,
    'conversation': state.conversation
  }
    

AutoPromptWhoIs = Tool(
  name="AutoPromptWhoIs",
  description="Make an automatic prompt for the WhoIs action",
  func=auto_prompt_who_is
)

