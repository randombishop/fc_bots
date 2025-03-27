from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_channel
from bots.data.channels import get_channel_by_url


parse_instructions_template = """
#TASK:
Your goal is to list the most active users in a social media channel.
Based on the provided context and instructions, which channel should we look at? 
You must only extract the channel parameter.
Channels typically start with / but not always.

#CURRENT CHANNEL: 
{{channel}}

#RESPONSE FORMAT:
{
  "channel": ...
}
"""

parse_schema = {
  "type":"OBJECT",
  "properties":{
    "channel":{"type":"STRING"}
  }
}


def parse(input):
  if input.state.params['channel_url'] is not None:
    return {'log': 'Channel already set'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_all()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  state.params['channel_url'] = read_channel(params, current_channel=state.root_parent_url, default_to_current=True)
  state.params['channel'] = get_channel_by_url(state.params['channel_url'])
  return {
    'channel_url': state.params['channel_url'],
    'channel': state.params['channel']
  }


ParseMostActiveUsersChannel = Tool(
  name="ParseMostActiveUsersChannel",
  description="Set the parameters channel_url and channel to run the MostActiveUsers tools.",
  func=parse
)
