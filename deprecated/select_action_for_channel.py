import random
from langchain.agents import Tool
from bots.data.bot_history import get_bot_actions_stats_in_channel


def select_action_for_channel(input):
  state = input.state
  action_rules = {
    'MostActiveUsers': {'min_hours': 240, 'min_activity': 50},
    'Perplexity': {'min_hours': 24, 'min_activity': 5},
    'Praise': {'min_hours': 24, 'min_activity': 10},
    'SaySomethingInChannel': {'min_hours': 24, 'min_activity': 15},
    'Summary': {'min_hours': 72, 'min_activity': 25}
  }
  candidates = get_bot_actions_stats_in_channel(state.id, state.selected_channel)
  candidates = {c['action_class']: {
    'hours_ago': float(c['hours_ago']) if c['hours_ago'] is not None else None,
    'channel_activity': int(c['channel_activity']) if c['channel_activity'] is not None else None,
    'is_valid': False
  } for c in candidates}
  for action, rules in action_rules.items():
    if action in candidates:
      valid_action1 = candidates[action]['hours_ago'] is None or candidates[action]['hours_ago'] > rules['min_hours']
      valid_action2 = candidates[action]['channel_activity'] is None or candidates[action]['channel_activity'] > rules['min_activity']
      candidates[action]['is_valid'] = valid_action1 and valid_action2
    else:
      candidates[action] = {'hours_ago': None, 'channel_activity': None, 'is_valid': True}
  valid_actions = [k for k,v in candidates.items() if v['is_valid']]
  if len(valid_actions) > 0:
    state.selected_action = random.choice(valid_actions)
  return {
    'selected_action': state.selected_action,
    'candidates': candidates,
    'valid_actions': valid_actions
  }  


SelectActionForChannel = Tool(
  name="SelectActionForChannel",
  func=select_action_for_channel,
  description="Select an action based on the channel"
)
