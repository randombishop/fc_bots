from langchain.agents import Tool
from bots.data.app import get_bot_config
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_boolean


prompt_template = """
#CONVERSATION
{{conversation}}

#LAST POST (your task is to decide if you like this post and return json: {"like": true/false})
{{request}}
"""

instructions_template = """
You are @{{name}} bot, a social media bot.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#TASK
Your task is to decide if the last post (=cast) in the provided conversation is worth liking.
prompt_like?
You must only evaluate if you should like the last message or ignore it.
You must respond with a json like this {"like": true/false}.
Use valid json format.

#OUTPUT FORMAT:
{
  "like": true/false
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "like":{"type":"BOOLEAN"}
  }
}



def like(input):
  state = input.state
  bot_config = get_bot_config(state.get('id'))
  if bot_config is None:
    return {
      'like': False, 
      'error': 'No Bot Config'
    }
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template).replace('prompt_like?', bot_config['prompt_like'])
  result = call_llm('medium', prompt, instructions, schema)
  like = read_boolean(result, key='like')
  return {
    'like': like
  }


Like = Tool(
  name="Like",
  description="Decide if you like a post",
  metadata={
    'outputs': ['like']
  },
  func=like
)