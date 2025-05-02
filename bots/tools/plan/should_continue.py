from langchain.agents import Tool
from bots.data.app import get_bot_config
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_boolean


instructions_template =  """
You are @{{name}}, a social media bot.

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


def should_continue(input):
  state = input.state
  bot_config = get_bot_config(state.get('id'))
  if bot_config is None:
    return {
      'should_continue': False, 
      'error': 'No Bot Config'
    }
  prompt_continue = bot_config['prompt_continue']
  if prompt_continue is None:
    prompt_continue = ''
  prompt = state.format_conversation()
  instructions = state.format(instructions_template).replace('prompt_continue?', prompt_continue)
  params = call_llm('medium', prompt, instructions, schema)
  should_continue = read_boolean(params, key='continue')
  return {
    'should_continue': should_continue
  }


ShouldContinue = Tool(
  name="ShouldContinue",
  func=should_continue,
  description="Evaluate if you should continue the conversation"
)