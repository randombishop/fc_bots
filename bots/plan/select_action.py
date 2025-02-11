from bots.i_plan_step import IPlanStep
from bots.utils.llms import call_llm


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
    print('use_channel')

  def use_no_channel(self):
    print('use_no_channel')

  def plan(self):
    if len(self.state.conversation)>0:
      self.use_conversation()
    elif self.state.channel is not None and self.state.channel not in ['', 'None']:
      self.use_channel()
    else:
      self.use_no_channel()
