from bots.utils.read_params import read_string
from bots.kit_interface.search_phrase import SearchPhrase
from bots.utils.format_state import format_template
from bots.utils.llms2 import call_llm


instructions = """
You are @{{bot_name}}

#TASK
You are currently executing a sequence of actions to prepare your response, and need to generate the search phrase parameter.
You must only generate the search phrase for now.
Output your generated search phrase in json format.
Make sure you don't use " inside json strings. 
Avoid invalid json.

RESPONSE FORMAT:
{
  "search_phrase": "..."
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "search_phrase":{"type":"STRING"}
  }
}


def new_search_phrase(search: str) -> SearchPhrase:
  params = {'search': search}
  search = read_string(params, key='search', max_length=500)
  return SearchPhrase(search)


def generate_search_phrase(bot_name: str, context: str, next_steps: str) -> SearchPhrase:
  prompt = context + '\n\n'
  prompt += '#NEXT STEPS TO EXECUTE\n'
  prompt += '(these will depend on the search phrase that you have to generate now)\n'
  prompt += next_steps
  instructions = format_template(instructions, {
    'bot_name': bot_name
  })
  result = call_llm('medium', prompt, instructions, schema)
  search = read_string(result, key='search_phrase', max_length=500)
  return new_search_phrase(search)

