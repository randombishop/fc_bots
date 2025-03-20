from langchain.agents import Tool
from bots.utils.llms2 import call_llm


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


def select_action_from_conversation(input):
  state = input.state
  llm = input.llm
  instructions = state.format(select_action_task)
  prompt = state.format(select_action_prompt)
  result = call_llm(llm, prompt, instructions, select_action_schema)
  if 'action' in result:
    state.selected_action = result['action']
  return {'selected_action': state.selected_action}
  

SelectActionFromConversation = Tool(
  name="select_action_from_conversation",
  func=select_action_from_conversation,
  description="Select an action based on the conversation",
  metadata={'depends_on': ['get_actions', 'get_conversation']}
)
