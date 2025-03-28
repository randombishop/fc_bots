from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_channel
from bots.data.channels import get_channel_by_url


parse_user_instructions_template = """
#TASK:
Based on the provided context and instructions, which channel should we look at? 
You must only extract the channel to be able to use your next tools.
You must only extract the channel parameter.
Channels typically start with / but not always.

current_channel?

#RESPONSE FORMAT:
{
  "channel": ...
}
"""

parse_user_schema = {
  "type":"OBJECT",
  "properties":{"user":{"type":"STRING"}}
}


def parse(input):
  state = input.state
  llm = input.llm
  parse_prompt = state.format_all()
  current_channel = state.get_current_channel()   
  current_channel = '#CURRENT CHANNEL:\n'+current_channel if current_channel is not None else ''
  parse_instructions = state.format(parse_user_instructions_template.replace('current_channel?', current_channel))
  params = call_llm(llm, parse_prompt, parse_instructions, parse_user_schema)
  channel_url = read_channel(params, current_channel=state.get('root_parent_url'), default_to_current=True)
  channel = get_channel_by_url(channel_url)
  return {
    'channel_url': channel_url,
    'channel': channel
  }
  

ParseChannel= Tool(
  name="ParseChannel",
  description="Set the parameters channel_url and channel to run the channel related tools.",
  metadata={
    'outputs': ['channel_url', 'channel']
  },
  func=parse
)
