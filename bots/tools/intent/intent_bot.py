import random
from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.intent.intents import get_intents, get_intents_descriptions, get_intended_targets, get_response_plan
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.helpers.tool_sequence import clean_tools, compile_sequence


instructions_template = """
#TASK
You are @{{name}}, a social media bot programmed to perform a specific set of actions.
Given the provided context and instructions, which intent most likely applies?
Your goal is not to continue the conversation directly, you must only select one of the following intents.
Pick one goal from the available options if it's explicitly asked for in the request, but if no specific intent is applicable, respond with {"intent": null}.
Do not pick the roast or psycho intents unless the user clearly asks for it, if not sure, avoid roast and psycho.
Focus on the intent of the last request, you can use the conversation for context but you are trying to decide the main intent here.
If no option is applicable, respond with {"intent": null}
Do not respond to the user, your task is only to figure out the intent.

#AVAILABLE OPTIONS:
available_intents?

#OUTPUT FORMAT
{
  "intent": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "intent":{"type":"STRING"}
  }
}

tool_map = {x.name: x for x in FETCH_TOOLS + PREPARE_TOOLS}

def select_intent(input):
  state = input.state
  instructions = state.format(instructions_template).replace('available_intents?', get_intents_descriptions())
  prompt = state.format_all(succint=True)
  result = call_llm('medium', prompt, instructions, schema)
  intent = result['intent'] if 'intent' in result else None
  if intent not in get_intents():
    intent = ''
  targets = get_intended_targets(intent)
  tools = clean_tools(targets, tool_map)
  tools, log = compile_sequence(state, tools)
  response_plan = get_response_plan(intent)
  return {
    'intent': intent, 
    'intended_targets': targets, 
    'intended_response_plan': response_plan,
    'todo': tools,
    'compile_log': log
  } 
  

IntentBot = Tool(
  name="IntentBot",
  description="Select current intent",
  metadata={
    'outputs': ['intent', 'intended_targets', 'intended_response_plan']
  },
  func=select_intent
) 
