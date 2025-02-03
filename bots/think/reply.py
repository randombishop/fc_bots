from bots.i_think_step import IThinkStep
from bots.utils.llms import call_llm
from bots.utils.read_params import read_boolean


prompt_template = """
#CONVERSATION
{{conversation}}

#POTENTIAL REPLY
{{casts}}

#TASK
Your task is to decide if the potential reply is good enough to be posted and return json: {"good_enough": true/false})
"""

instructions_template = """
You are @{{name}} bot, a social media bot.
Your task is to decide if the prepared reply is good enough to be posted.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

INSTRUCTIONS:
If it's a valid reply that makes sense, set good_enough to true.
If the potential reply sounds good to you, set good_enough to true.
If the reply is funny, set good_enough to true.
If the reply is somehow relevant to the conversation, set good_enough to true.
If it doesn't make sense, set good_enough to false.
If the conversation is going in circles, set good_enough to false.
If the conversation is getting repetitive, boring, aggressive, offensive or not constructive, set good_enough to false.
If you're not sure, set good_enough to false.

OUTPUT FORMAT:
{
  "good_enough": true/false
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "good_enough":{"type":"BOOLEAN"}
  }
}



class Reply(IThinkStep):
      
  def think(self):
    prompt = self.state.format(prompt_template)
    instructions = self.state.format(instructions_template)
    result = call_llm(prompt, instructions, schema)
    self.state.reply = read_boolean(result, key='good_enough')
    print('<---------------------------- Reply Validation ---------------------------->')
    print(prompt)
    #print('---------------------------------------------------------------------------')
    #print(instructions)
    #print('---------------------------------------------------------------------------')
    #print(result)
    print(f"<---------------------------- state.reply = {self.state.reply} ---------------------------->")
