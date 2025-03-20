from langchain.agents import Tool
from bots.utils.call_llm import call_llm
from bots.utils.read_params import read_boolean


prompt_template = """
#CONVERSATION
{{conversation}}

#LAST POST (your task is to decide if you like this post and return json: {"like": true/false})
{{request}}
"""

instructions_template = """
You are @{{name}} bot, a social media bot.
Your task is to decide if the last post (=cast) in the provided conversation is worth liking.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

INSTRUCTIONS:
If it's a greeting or a thank you message, set "like" to true. 
If it's a positive message or interesting feedback about the conversation, set "like" to true.  
If it's a nice reference to your bio or lore, set "like" to true.
Otherwise, set "like" to false.

OUTPUT FORMAT:
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
  state = input['state']
  llm = input['llm']
  if not state.is_responding:
    return
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  state.like = read_boolean(result, key='like')
  return {
    'like': state.like
  }


Like = Tool(
  name="Like",
  description="Decide if you like a post",
  func=like
)