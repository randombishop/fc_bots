from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.kit_impl.fetch.get_capabilities import get_intents, get_intents_descriptions, get_response_plan
from bots.kit_impl.fetch.get_source_code import get_source_code
from bots.utils.format_state import format_template, format_state
from bots.utils.functions import validate_sequence


instructions_template = """
#TASK
You are @{{bot_name}}, a social media bot with access to a set of tools.
Given the provided context and instructions, your task is to generate your own plan before responding to the user.
Your goal is not to continue the conversation directly, you must only plan and prepare yourself.
Study the context, conversation and instructions to understand the user's intent.
Study your source code to understand your capabilities.
You have access to your own state variables and you can run the state.execute() function to call methods from Fetch and Prepare implementations.
Study your current state variables to understand your current progress towards your goal.
Once you have a full understanding of your current goal, state and capabilities, you can decide if you want to execute a program or proceed to composing your answer.
If you are ready to compose your answer, just output {"program": []}
If you decide to execute a program, write a program that will be successfully executed and output the sequence of calls in json format.
Your program must be a sequence of calls to execute(tool: str, method: str, str_params: dict, var_params: dict, variable_name: str, variable_description: str)
- tool: str - The tool implementation to use (fetch or prepare)
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

schema = {
  "type":"OBJECT",
  "properties":{
    "program":{"type":"ARRAY"}
  }
}


def _plan(state):
  state.iterations += 1
  instructions = format_template(instructions_template, {'bot_name': state.bot_name})
  prompt = format_state(state, intro=True, variables=True)
  if len(state.get_variable_values('SourceCode'))==0:
    prompt += '\n\n\n' + '-'*100 + '\n\n\n'
    prompt += '# YOUR SOURCE CODE:\n\n'
    prompt += str(get_source_code())
    prompt += '\n\n'  
  result = call_llm('large', prompt, instructions, schema) 
  program = result['program'] if 'program' in result else []
  validated, error = validate_sequence(state, program) 
  plan = {
    'program': program,
    'validated': validated.copy(),
    'error': error
  } 
  state.plan = plan
  state.todo = validated
  return plan

plan = Tool(
  name="plan",
  description="Generate a plan",
  func=_plan
) 
