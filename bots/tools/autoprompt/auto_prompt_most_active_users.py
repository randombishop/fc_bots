from langchain.agents import Tool
from bots.data.channels import get_channel_url


def auto_prompt_most_active_users(input):
  state = input.state
  channel_url = get_channel_url(state.selected_channel)
  if channel_url is None:
    raise Exception("Most Active Users autoprompt can't find channel_url")
  state.action_params = {'channel': channel_url}
  state.request = f'Most active users in channel /{state.selected_channel}'
  state.conversation = state.request
  return {
    'action_params': state.action_params,
    'request': state.request,
    'conversation': state.conversation
  }


AutoPromptMostActiveUsers = Tool(
  name="auto_prompt_most_active_users",
  description="Create an automatic prompt for the most active users action",
  func=auto_prompt_most_active_users
)
