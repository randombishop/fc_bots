from langchain.agents import Tool
from bots.utils.llms2 import call_llm

select_action_prompt = """
#YOUR INSTRUCTIONS
{{instructions}}
"""

select_action_task = """
#INSTRUCTIONS
You are @{{name}}, a social media bot with access to a set of actions.
Given the provided context and instructions, which action can help you with the instructions?
Your goal is not to respond to the instructions directly, you must only decide which action to execute to gain more data.
Decide the action that should be used before responding to the instructions.
Even if no action directly applies to the instructions, pick one that can provide more data and be indirectly used to generate a better post.
If no action is applicable, respond with {"action": null}
Also provide a reasoning for your choice.

#AVAILABLE TOOLS:
{{actions}}

#OUTPUT FORMAT
{
  "action": "...",
  "reasoning": "..."
}
"""

select_action_schema = {
  "type":"OBJECT",
  "properties":{
    "action":{"type":"STRING"},
    "reasoning":{"type":"STRING"}
  }
}




def select_action_from_instructions(input):
  state = input.state
  llm = input.llm
  if state.instructions is None or len(state.instructions) == 0:
    raise Exception('No instructions provided')
  instructions = state.format(select_action_task)
  prompt = state.format(select_action_prompt)
  result = call_llm(llm, prompt, instructions, select_action_schema)
  if 'action' in result:
    state.action = result['action']
  if 'reasoning' in result:
    state.action_reasoning = result['reasoning']
  return {
    'action': state.action, 
    'action_reasoning': state.action_reasoning
  }
  

SelectActionFromInstructions = Tool(
  name="SelectActionFromInstructions",
  func=select_action_from_instructions,
  description="Select an action based on the instructions"
)
