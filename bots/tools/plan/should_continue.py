from langchain.agents import Tool
from bots.utils.llms2 import call_llm
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
{{selected_channel}}

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


def should_continue(input):
  state = input.state
  llm = input.llm
  prompt = state.format_conversation()
  instructions = state.format(instructions_template)
  params = call_llm(llm, prompt, instructions, schema)
  state.should_continue = read_boolean(params, key='continue')
  return {'should_continue': state.should_continue}


ShouldContinue = Tool(
  name="ShouldContinue",
  func=should_continue,
  description="Evaluate if you should continue the conversation"
)