from bots.i_prepare_step import IPrepareStep
from bots.prompts.contexts import conversation_and_request_template
from bots.utils.llms import call_llm
from bots.utils.read_params import read_boolean


instructions_template =  """
You are @{{name}}, a social media bot.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#CURRENT CHANNEL
{{channel}}

#TASK
Before responding to the user, you must evaluate if you should continue this conversation or not. 
If the user asks an interesting question or if their tone elicits a response from you, you should continue the conversation.
If the conversation is going in a contructive direction and produces interesting information from both sides, you should continue the conversation.
If it's just a greeting, a thank you note, or a closing comment, you should not continue the conversation.
If the conversation is not constructive, enters some kind of loop, or is not going anywhere, you should not continue the conversation.
If the conversation has been going back and forth for more than 10 messages without any progress, you should not continue the conversation.
You must only evaluate if you should continue the conversation or ignore the last request.
You must respond with a json like this {"continue": true/false}.
Return your evaluation in valid json format.

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


class ShouldContinue(IPrepareStep):
    
  def prepare(self):
    prompt = self.state.format(conversation_and_request_template)
    instructions = self.state.format(instructions_template)
    params = call_llm(prompt, instructions, schema)
    self.state.should_continue = read_boolean(params, key='continue')
    print('self.state.should_continue=', self.state.should_continue)

  