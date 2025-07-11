from langchain.agents import Tool
from bots.utils.format_state import format_template, format_state
from bots.utils.format_cast import format_casts
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_boolean, read_string


instructions_template = """
# TASK
You are @{{bot_name}} bot
Your goal is to validate your own process before posting on a social media platform.
FYI, posts are called casts in farcaster.
Your task is to decide if you should block the prepared casts before posting.
The reasons for blocking are: off-topic, repetitive, boring, aggressive or misunderstanding.
Analyze the provided context, instructions and your prepared posts, and decide if you want to move forward with casting them.
If your casts are completely off-topic, set do_not_post=true and reason="off-topic".
If the conversation is going in circles, set do_not_post=true and reason="repetitive".
If the conversation is getting boring, set do_not_post=true and reason="boring".
If the conversation is getting aggressive, set do_not_post=true and reason="aggressive".
If there is a misunderstanding or mismatch between the instructions intent and your prepared output, set do_not_post=true and reason="misunderstanding".
If the last request explicitly asked for roasting or psycho analysis, expect the reply to be parodic and roasting and set do_not_post=false and reason="".
If your reply is good enough to continue the conversation, set do_not_post=false and reason="".
If your posts looks fine, set do_not_post=false and reason="" even if it's not perfect.
If you are not confident that one of the blocking reasons applies, set do_not_post=false and reason="".

OUTPUT FORMAT:
{
  "do_not_post": true/false,
  "reason": "if do_not_post=true, pick one of the following reasons: off-topic, repetitive, boring, aggressive, misunderstanding. If do_not_post is false, set to an empty string."
}
"""


schema = {
  "type":"OBJECT",
  "properties":{
    "do_not_post":{"type":"BOOLEAN"},
    "reason":{"type":"STRING"}
  }
}


def _check(state):
  state.checked = True
  bot_name = state.bot_name
  
  casts = format_casts(state.casts)
  instructions = format_template(instructions_template, {'bot_name': bot_name})
  prompt = format_state(state, intro=False, variables=False)
  prompt += f'\n\n#PREPARED POSTS:\n{casts}'
  result = call_llm('medium', prompt, instructions, schema)
  do_not_post = read_boolean(result, key='do_not_post')
  reason = read_string(result, key='reason')
  valid = (not do_not_post)
  state.valid = valid
  return {
    'valid': valid,
    'do_not_post_reason': reason
  }
    

check = Tool(
  name="check",
  description="Check casts",
  func=_check
)