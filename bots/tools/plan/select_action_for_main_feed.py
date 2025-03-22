import random
from langchain.agents import Tool
from bots.data.bot_history import get_bot_actions_stats_no_channel

 
def select_action_for_main_feed(input):
  state = input.state
  action_rules = {
    'Perplexity': {'min_hours': 6},
    'SaySomethingNoChannel': {'min_hours': 12},
    'Praise': {'min_hours': 24},
    'Summary': {'min_hours': 24}
  }
  candidates = get_bot_actions_stats_no_channel(state.id)
  candidates = {c['action_class']: {
      'hours_ago': float(c['hours_ago']) if c['hours_ago'] is not None else None,
      'is_valid': False
    } for c in candidates}
  for action, rules in action_rules.items():
    if action in candidates:
      valid_action = candidates[action]['hours_ago'] is None or candidates[action]['hours_ago'] > rules['min_hours']
      candidates[action]['is_valid'] = valid_action
    else:
      candidates[action] = {'hours_ago': None, 'is_valid': True}
  valid_actions = [k for k,v in candidates.items() if v['is_valid']]
  if len(valid_actions) > 0:
    state.selected_action = random.choice(valid_actions)
  return {
    'selected_action': state.selected_action,
    'candidates': candidates,
    'valid_actions': valid_actions
  }


SelectActionForMainFeed = Tool(
  name="SelectActionForMainFeed",
  func=select_action_for_main_feed,
  description="Select an action for the main feed"
)
