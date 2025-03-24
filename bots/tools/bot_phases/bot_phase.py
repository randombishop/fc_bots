from bots.tools.actions import ACTION_CONFIG


def get_action_config_tools(action, phase):
  if action is None or action not in ACTION_CONFIG:
    return None
  config = ACTION_CONFIG[action]
  return config[phase] if phase in config else None


def run_phase(input, phase, tools):
  tool_map = {t.name: t for t in tools}
  state = input.state
  selected_action = state.action
  if selected_action is None:
    return {'log': 'No action selected'}
  tools = get_action_config_tools(selected_action, phase)
  if tools is None:
    return {'log': f'No tools configured for {selected_action}'}
  for t in tools:
    tool = tool_map[t]
    tool.invoke({'input': input})
  return {
    'tools': tools
  }