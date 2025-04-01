from langchain.agents import Tool
from bots.data.bot_history import get_random_user, get_random_user_in_channel
from bots.data.users import get_fid


def parse(input):
  state = input.state
  bot_id = state.get('id')
  channel_url = state.get('channel_url')
  user_name, fid = None, None
  if channel_url is None:
    user_name = get_random_user(bot_id)
    fid = get_fid(user_name)  
  else:
    user_name = get_random_user_in_channel(bot_id, channel_url)
    fid = get_fid(user_name)
  return {
    'user_fid': fid,
    'user': user_name
  }
  
desc = """Select a random user and set user_fid and user to run any user related tools.
If the instructions specifically require selecting a random user, use SelectRandomUser."""

SelectRandomUser = Tool(
  name="SelectRandomUser",
  description=desc,
  metadata={
    'outputs': ['user_fid', 'user']
  },
  func=parse
)
