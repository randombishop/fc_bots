from bots.data.app import get_bot_config
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_boolean
from bots.utils.prompts import format_template


prompt_template = """
#CONVERSATION
{{conversation}}

#LAST POST (your task is to decide if you like this post and return json: {"like": true/false})
{{request}}
"""

instructions_template = """
You are @{{bot_name}} bot, a social media bot.

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



def like(bot_id, bot_name, bio, lore, conversation, request):
  bot_config = get_bot_config(bot_id)
  if bot_config is None:
    return False
  prompt = format_template(prompt_template, {'conversation': conversation, 'request': request})
  instructions = format_template(instructions_template, {'bot_name': bot_name, 'bio': bio, 'lore': lore}).replace('prompt_like?', bot_config['prompt_like'])
  result = call_llm('medium', prompt, instructions, schema)
  like = read_boolean(result, key='like')
  return like

