from langchain.agents import Tool


def select_action_mode(input):
  state = input.state
  if state.request is not None and len(state.request)>0:
    state.selected_action_mode = 'conversation'
  elif state.selected_channel is not None and state.selected_channel not in ['', 'None']:
    state.selected_action_mode = 'channel'
  else:
    state.selected_action_mode = 'main_feed'
  return {
    'selected_action_mode': state.selected_action_mode
  }


SelectActionMode = Tool(
  name="SelectActionMode",
  func=select_action_mode,
  description="Select an action mode to choose from conversation, channel or main feed"
)
