import random
from bots.i_plan_step import IPlanStep
from bots.utils.llms import call_llm
from bots.data.bot_history import get_bot_actions_stats_in_channel, get_bot_actions_stats_no_channel

select_action_task = """
#INSTRUCTIONS
You are @{{name}}, a social media bot programmed to perform a specific set of actions.
Given the provided conversation and request, which action should you perform next?
Your goal is not to continue the conversation directly, you must only decide which action to perform.
Decide the action that matches the requests's intent.
Pick one specific action from the available options if it's explicitly asked for in the request, but if no specific action is applicable, respond with {"action": null}.
Do not pick the roast or psychoanalyze actions unless the user clearly asks for it, if not sure, avoid the Roast and Psycho actions.
Focus on the intent of the last request, you can use the conversation for context but you are trying to decide which action to perform based on the final request.
If no action is applicable, respond with {"action": null}

#AVAILABLE ACTIONS:
{{actions}}

#OUTPUT FORMAT
{
  "action": "..."
}
"""

select_action_schema = {
  "type":"OBJECT",
  "properties":{
    "action":{"type":"STRING"}
  }
}

select_action_prompt = """
#CONVERSATION
{{conversation}}

#REQUEST
{{request}}
"""


class SelectAction(IPlanStep):

  def use_conversation(self):
    instructions = self.state.format(select_action_task)
    prompt = self.state.format(select_action_prompt)
    result = call_llm(prompt, instructions, select_action_schema)
    if 'action' in result:
      self.state.selected_action = result['action']

  def use_channel(self):
    action_rules = {
      'MostActiveUsers': {'min_hours': 240, 'min_activity': 50},
      'Perplexity': {'min_hours': 24, 'min_activity': 5},
      'Praise': {'min_hours': 24, 'min_activity': 10},
      'SaySomethingInChannel': {'min_hours': 24, 'min_activity': 15},
      'Summary': {'min_hours': 72, 'min_activity': 25}
    }
    candidates = get_bot_actions_stats_in_channel(self.state.id, self.state.channel)
    candidates = {c['action_class']: {
        'hours_ago': float(c['hours_ago']) if c['hours_ago'] is not None else None,
        'channel_activity': int(c['channel_activity']) if c['channel_activity'] is not None else None
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
      self.state.selected_action = random.choice(valid_actions)
    self.state.log += '<SelectAction branch="channel">\n'
    self.state.log += 'SelectAction.use_channel()\n'
    self.state.log += 'candidate actions:\n'
    for c in candidates:
      self.state.log += '  ' + c + ': ' + str(candidates[c]) + '\n'
    self.state.log += 'valid actions:' + str(valid_actions) + '\n'
    self.state.log += '</SelectAction selected="{self.state.selected_action}">\n'
    

  def use_no_channel(self):
    action_rules = {
      'Perplexity': {'min_hours': 6},
      'SaySomethingNoChannel': {'min_hours': 12},
      'Praise': {'min_hours': 24},
      'Summary': {'min_hours': 24}
    }
    candidates = get_bot_actions_stats_no_channel(self.state.id)
    candidates = {c['action_class']: {
        'hours_ago': float(c['hours_ago']) if c['hours_ago'] is not None else None
      } for c in candidates}
    for action, rules in action_rules.items():
      if action in candidates:
        valid_action = candidates[action]['hours_ago'] is None or candidates[action]['hours_ago'] > rules['min_hours']
        candidates[action]['is_valid'] = valid_action
      else:
        candidates[action] = {'hours_ago': None, 'is_valid': True}
    valid_actions = [k for k,v in candidates.items() if v['is_valid']]
    if len(valid_actions) > 0:
      self.state.selected_action = random.choice(valid_actions)
    self.state.log += '<SelectAction branch="no_channel">\n'
    self.state.log += 'SelectAction.no_channel()\n'
    self.state.log += 'candidate actions:\n'
    for c in candidates:
      self.state.log += '  ' + c + ': ' + str(candidates[c]) + '\n'
    self.state.log += 'valid actions:' + str(valid_actions) + '\n'
    self.state.log += '</SelectAction selected="{self.state.selected_action}">\n'

  def plan(self):
    if len(self.state.conversation)>0:
      self.use_conversation()
    elif self.state.selected_channel is not None and self.state.selected_channel not in ['', 'None']:
      self.use_channel()
    else:
      self.use_no_channel()
