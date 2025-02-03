from bots.i_think_step import IThinkStep
from bots.utils.llms import call_llm
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



class Like(IThinkStep):
      
  def think(self):
    prompt = self.state.format(prompt_template)
    instructions = self.state.format(instructions_template)
    result = call_llm(prompt, instructions, schema)
    self.state.like = read_boolean(result, key='like')
