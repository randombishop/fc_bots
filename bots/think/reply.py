from bots.i_think_step import IThinkStep
from bots.utils.llms import call_llm
from bots.utils.read_params import read_boolean


prompt_template = """
#CONVERSATION
{{conversation}}

#POTENTIAL REPLY (your task is to decide if this reply is valid and return json: {"valid": true/false})
{{casts}}
"""

instructions_template = """
You are @{{name}} bot, a social media bot.
Your task is to decide if the prepared reply is good enough to be posted as a reply.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

INSTRUCTIONS:
If it's a valid reply that makes sense, set valid_reply to true.
If the potential reply sounds good to you, set valid_reply to true.
If the reply is consistent with your bio, lore or style, set valid_reply to true.
If the reply is funny, set valid_reply to true.
If it doesn't make sense or confusing, set valid_reply to false.
If the conversation is going in circles, set valid_reply to false.
If the conversation is getting repetitive, boring, aggressive, offensive or not constructive, set valid_reply to false.
If you're not sure, set valid_reply to false.

OUTPUT FORMAT:
{
  "valid_reply": true/false
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "valid_reply":{"type":"BOOLEAN"}
  }
}



class Reply(IThinkStep):
      
  def think(self):
    prompt = self.state.format(prompt_template)
    instructions = self.state.format(instructions_template)
    result = call_llm(prompt, instructions, schema)
    self.state.reply = read_boolean(result, key='valid_reply')
    print('<---------------------------- Reply Validation ---------------------------->')
    print(prompt)
    print(f"<---------------------------- state.reply = {self.state.reply} ---------------------------->")
