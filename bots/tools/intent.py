import os
from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.intents import get_intents, get_intents_descriptions, get_intended_targets, get_response_plan
from bots.utils.prompts import format_template



instructions_template1 = """
#TASK
You are @{{bot_name}}, a social media bot programmed to perform a specific set of actions.
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

schema1 = {
  "type":"OBJECT",
  "properties":{
    "intent":{"type":"STRING"}
  }
}

instructions_template2 = """
#TASK
You are @{{bot_name}}, a social media bot with access to a set of tools.
Given the provided context and instructions, your task is to write a program to leverage your tools before responding to the user.
Your goal is not to continue the conversation directly, you must only write a program to prepare yourself.
You have access to your own state variables and you can run the state.execute() function to call methods from Fetch and Prepare implementations.
Study your source code to understand your capabilities and write a program that will be successfully executed.
Your program must be a sequence of calls to execute(tool: str, method: str, str_params: dict, var_params: dict, variable_name: str, variable_description: str)
- tool: str - The tool implementation to use (fetch or prepare)
- method: str - The method to execute (see the tool implementation for details)
- str_params: dict - The string parameters to pass to the method - You can pass any string here. (optional)
- var_params: dict - The variable references to pass to the method, these must be available in self.variables, make sure you simulate what you ran before to evaluate if a variable will be available at any point in time. (optional)
- variable_name: str - The name of the variable to set with the result of the method (optional) - Where do you want to store the result of the execution?
- variable_description: str - The description of the obtained variable (optional) - What is the purpose of the variable?
{{intended_targets}}
Your task is to figure out the prerequisites and parameters of the intended targets and compose a program that will successfully execute its final steps.
Make sure all required parameters are prepared by previous steps before each new call.
You must output your sequence of calls as a list of dictionaries in json format.



#OUTPUT FORMAT
[
  {
    "tool": "...",
    "method": "...",
    "str_params": {
      "...": "..."
    },
    "var_params": {
      "...": "..."
    },
    "variable_name": "...",
    "variable_description": "..."
  },
  ...
]
"""

schema2 = {
  "type":"ARRAY"
}

def get_source_code(folder, file, package):
  ans = ''
  current_dir = os.path.dirname(os.path.abspath(__file__))
  state_file = os.path.join(current_dir, folder, file)
  with open(state_file, 'r') as f:
    ans += f"### {package}.{file[:-3]} ###'\n"
    ans += f.read() + '\n'
    ans += f"### End of {file} ###'\n"
  return ans


def select_intent(state):
  state.iterations = 'done'
  instructions1 = format_template(instructions_template1, {'bot_name': state.bot_name}).replace('available_intents?', get_intents_descriptions())
  prompt1 = state.get_context()
  result1 = call_llm('medium', prompt1, instructions1, schema1)
  intent = result1['intent'] if 'intent' in result1 else None
  if intent not in get_intents():
    intent = ''
  targets = get_intended_targets(intent)
  response_plan = get_response_plan(intent)
  if targets is not None and len(targets) > 0:
    targets_str = "Your sequence should finish with these target calls:\n"
    for t in targets:
      targets_str += f"- {t['tool']}.{t['method']}\n"
  else:
    targets_str = ''
  instructions2 = format_template(instructions_template2, {'bot_name': state.bot_name, 'intended_targets': targets_str})
  prompt2 = state.get_context()
  prompt2 += '\n\n\n' + '-'*100 + '\n\n\n'
  prompt2 += '# YOUR SOURCE CODE:\n\n'
  kit_interface_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../kit_interface')
  for file in os.listdir(kit_interface_dir):
    if file.endswith('.py'):
      prompt2 += get_source_code('../kit_interface', file, 'bots.kit_interface') + '\n'
  prompt2 += get_source_code('../kit_entrypoint', 'fetch.py', 'bots.kit_entrypoint') + '\n'
  prompt2 += get_source_code('../kit_entrypoint', 'prepare.py', 'bots.kit_entrypoint') + '\n'
  prompt2 += get_source_code('..', 'state.py', 'bots') + '\n'
  result2 = call_llm('medium', prompt2, instructions2, schema2) 
  return {
    'intent': intent, 
    'intended_targets': targets, 
    'intended_response_plan': response_plan,
    'program': result2
  } 
  

intent = Tool(
  name="intent",
  description="Select current intent",
  func=select_intent
) 
