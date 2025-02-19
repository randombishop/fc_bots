from bots.i_think_step import IThinkStep
from bots.utils.llms import call_llm
from bots.utils.read_params import read_boolean, read_string


prompt_template = """
#CONVERSATION
{{conversation}}

#POTENTIAL REPLY
{{casts}}
"""

instructions_template = """
You are @{{name}} bot, a social media bot on the farcaster platform.
FYI, in the farcaster platform, posts are called casts.
Your task is to decide if you should block the potential reply before posting it.
The reasons for blocking a reply are: off-topic, repetitive, boring, aggressive or misunderstanding.

INSTRUCTIONS:
If the potential reply is completely off-topic, set do_not_reply=true and reason="off-topic".
If the conversation is going in circles, set do_not_reply=true and reason="repetitive".
If the conversation is getting boring, set do_not_reply=true and reason="boring".
If the conversation is getting aggressive, set do_not_reply=true and reason="aggressive".
If there is a misunderstanding between the user and you, set do_not_reply=true and reason="misunderstanding".
If the last request explicitly asked for roasting or psycho analysis, expect the reply to be parodic and roasting and set do_not_reply=false and reason="".
If the reply is good enough to continue the conversation, set do_not_reply=false and reason="".
If the reply looks fine, set do_not_reply=false and reason="" even if it's not perfect.
If you are not confident that one of the blocking reasons applies, set do_not_reply=false and reason="".

OUTPUT FORMAT:
{
  "do_not_reply": true/false,
  "reason": "if do_not_reply=true, pick one of the following reasons: off-topic, repetitive, boring, aggressive, misunderstanding. If do_not_reply is false, set to an empty string."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "do_not_reply":{"type":"BOOLEAN"},
    "reason":{"type":"STRING"}
  }
}



class Reply(IThinkStep):
      
  def think(self):
    prompt = self.state.format(prompt_template)
    instructions = self.state.format(instructions_template)
    result = call_llm(prompt, instructions, schema)
    do_not_reply = read_boolean(result, key='do_not_reply')
    reason = read_string(result, key='reason', default='')
    self.state.reply = (not do_not_reply)
    if do_not_reply:
      self.state.do_not_reply_reason = reason
    