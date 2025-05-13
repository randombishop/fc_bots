from bots.utils.read_params import read_keyword
from bots.kit_interface.keyword import Keyword
from bots.utils.format_state import format_template
from bots.utils.llms2 import call_llm


instructions_template = """
You are @{{bot_name}}, an AI agent with access to a set of tools, currently executing a sequence of actions to prepare your response.

#TASK
First study your current state, context, instructions and planned next steps. 
Your current task is to generate a keyword parameter.
Which keyword should we use for next steps?
Do not use an abbreviation for the keyword, it has to be at least 4 characters long.
The keyword should be a single word, not a phrase.
You don't have to respond to the main goal directly, you must only focus on generating the keyword.
Output your generated keyword in json format.
Make sure you don't use " inside json strings. 
Avoid invalid json.

RESPONSE FORMAT:
{
  "keyword": "..."
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "keyword":{"type":"STRING"}
  }
}


def new_keyword(keyword: str) -> Keyword:
  params = {'keyword': keyword}
  keyword = read_keyword(params)
  return Keyword(keyword)


def generate_keyword(bot_name: str, context: str, next_steps: str) -> Keyword:
  prompt = context + '\n\n'
  prompt += '#NEXT STEPS TO EXECUTE\n'
  prompt += '(these will depend on the keyword that you have to pick now)\n'
  prompt += next_steps
  instructions = format_template(instructions_template, {
    'bot_name': bot_name
  })
  result = call_llm('medium', prompt, instructions, schema)
  keyword = read_keyword(result)
  return Keyword(keyword)