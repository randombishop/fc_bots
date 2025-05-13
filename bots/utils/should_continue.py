from bots.data.app import get_bot_config
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_boolean
from bots.utils.format_state import format_conversation, format_template


instructions_template =  """
You are @{{bot_name}}, a social media bot.

#TASK
Before responding to the user, you must evaluate if you should continue this conversation or not. 
You must only evaluate if you should continue the conversation or ignore it.
prompt_continue?
You must respond with a json like this {"continue": true/false}.
Use valid json format.


#RESPONSE FORMAT
{
  "continue": true/false
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "continue":{"type":"BOOLEAN"}
  }
}


def should_continue(bot_id, bot_name, channel, conversation, request):
  bot_config = get_bot_config(bot_id)
  if bot_config is None:
    return {
      'should_continue': False, 
      'error': 'No Bot Config'
    }
  prompt_continue = bot_config['prompt_continue']
  if prompt_continue is None:
    prompt_continue = ''
  prompt = format_conversation(channel, conversation, request)
  instructions = format_template(instructions_template, {'bot_name': bot_name}).replace('prompt_continue?', prompt_continue)
  params = call_llm('medium', prompt, instructions, schema)
  return read_boolean(params, key='continue')

