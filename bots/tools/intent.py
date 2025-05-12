import os
from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.kit_impl.fetch.get_capabilities import get_intents, get_intents_descriptions, get_response_plan
from bots.kit_impl.fetch.get_source_code import get_source_code
from bots.utils.format_state import format_template, format_state
from bots.utils.functions import validate_sequence



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
You have access to your own state variables and you can run the state.execute() function to call methods from Fetch, Prepare and MiniApps implementations.
Study your source code to understand your capabilities and write a program that will be successfully executed.
Your program must be a sequence of calls to execute(tool: str, method: str, str_params: dict, var_params: dict, variable_name: str, variable_description: str)
- tool: str - The tool implementation to use (fetch, prepare or miniapps)
- method: str - The method to execute (see the tool implementation for details)
- str_params: dict - The string parameters to pass to the method - You can pass any string here. (optional)
- var_params: dict - The variable references to pass to the method, these must be available in self.variables, make sure you simulate what you ran before to evaluate if a variable will be available at any point in time. (optional)
- variable_name: str - The name of the variable to set with the result of the method (*required, you must set a target variable name to be able to see the result) - Where do you want to store the result of the execution?
- variable_description: str - The description of the obtained variable (optional) - What is the purpose of the variable?
Your task is to figure out the prerequisites and parameters of the intended targets and compose a program that will successfully execute.
Once you prepared your call sequence, simulate it and calculate available variables after each step.
Make sure all required parameters are made available by previous steps before each new call.
You must output your sequence of calls as a list of dictionaries in json format.
Once you have prepared and formatted your program in json format, double check that the json is valid.

{{response_plan}}

#OUTPUT FORMAT
{
  "program": [
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
}
"""

schema2 = {
  "type":"OBJECT",
  "properties":{
    "program":{"type":"ARRAY"}
  }
}


def select_intent(state):
  state.iterations = 'done'
  instructions1 = format_template(instructions_template1, {'bot_name': state.bot_name}).replace('available_intents?', get_intents_descriptions())
  prompt1 = format_state(state, intro=True, variables=True)
  result1 = call_llm('medium', prompt1, instructions1, schema1)
  intent = result1['intent'] if 'intent' in result1 else None
  if intent not in get_intents():
    intent = ''
  response_plan = get_response_plan(intent)
  instructions2 = format_template(instructions_template2, {
    'bot_name': state.bot_name, 
    'response_plan': f"#SUGGESTED RESPONSE PLAN\n{response_plan}"}
    )
  prompt2 = format_state(state, intro=True, variables=True)
  if len(state.get_variable_values('SourceCode'))==0:
    prompt2 += '\n\n\n' + '-'*100 + '\n\n\n'
    prompt2 += '# YOUR SOURCE CODE:\n\n'
    prompt2 += str(get_source_code())
    prompt2 += '\n\n'
  prompt2 += f"#SUGGESTED RESPONSE PLAN\n{response_plan}"
  result2 = call_llm('large', prompt2, instructions2, schema2) 
  program = result2['program'] if 'program' in result2 else []
  validated, error = validate_sequence(state, program) 
  plan = {
    'intent': intent, 
    'response_plan': response_plan,
    'program': program,
    'validated': validated.copy(),
    'error': error
  } 
  state.plan = plan
  state.todo = validated
  return plan

intent = Tool(
  name="intent",
  description="Select current intent",
  func=select_intent
) 
