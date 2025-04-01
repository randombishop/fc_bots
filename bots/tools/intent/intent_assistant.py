import random
from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.helpers.tool_sequence import format_tool
from bots.tools.intent.intents import get_intent_examples, DEFAULT_ACTION_PLAN, DEFAULT_RESPONSE_PLAN

instructions_template = """
#TASK
You are @{{name}}, a social media bot programmed to do scheduled posts on a social media channel.
Given the provided context and instructions, your task is to come up with a plan for your next post.
Your goal is to understand the intent of your instructions, prepare your action plan, and think about what you want to post.  
You are provided with a series of examples of plans for reference, but you don't have to follow them exactly.
You are also provided with a list of available tools so that you know your possibilities.
Output 3 fields in json format: 
- intent: one word title for your plan
- intended_action_plan: the steps you plan to take
- intended_response_plan: how you think your response should look like

#EXAMPLES:
intent_examples?

#AVAILABLE TOOLS:
available_tools?

#OUTPUT FORMAT
{
  "intent": "...",
  "intended_action_plan": "...",
  "intended_response_plan": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "intent":{"type":"STRING"}
  }
}


def select_intent(input):
  state = input.state
  llm = input.llm
  instructions = state.format(instructions_template)
  examples = get_intent_examples()
  instructions = instructions.replace('intent_examples?', examples)
  tools = PARSE_TOOLS+FETCH_TOOLS+PREPARE_TOOLS
  tools = "\n".join([format_tool(tool) for tool in tools])
  instructions = instructions.replace('available_tools?', tools)
  prompt = state.format_all(succint=True)
  result = call_llm(llm, prompt, instructions, schema)
  intent = result['intent'] if 'intent' in result else ''
  action_plan = result['intended_action_plan'] if 'intended_action_plan' in result else DEFAULT_ACTION_PLAN
  response_plan = result['intended_response_plan'] if 'intended_response_plan' in result else DEFAULT_RESPONSE_PLAN
  return {
    'intent': intent, 
    'intended_action_plan': action_plan, 
    'intended_response_plan': response_plan
  } 
  

IntentAssistant = Tool(
  name="IntentAssistant",
  description="Select current intent",
  metadata={
    'outputs': ['intent', 'intended_action_plan', 'intended_response_plan']
  },
  func=select_intent
) 
