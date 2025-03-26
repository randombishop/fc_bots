from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_channel
from bots.data.channels import get_channel_by_url


parse_instructions_template = """
#TASK:
You are @{{name}}, a bot programmed to list the most active users in a social media channel.
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


def parse_most_active_users(input):
  if input.state.channel is not None:
    return {'log': 'Channel already set'}
  state = input.state
  llm = input.llm
  parse_prompt = state.format_prompt()
  parse_instructions = state.format(parse_instructions_template)
  params = call_llm(llm, parse_prompt, parse_instructions, parse_schema)
  state.channel_url = read_channel(params, current_channel=state.root_parent_url, default_to_current=True)
  state.channel = get_channel_by_url(state.channel_url)
  return {
    'channel_url': state.channel_url,
    'channel': state.channel
  }


ParseMostActiveUsersParams = Tool(
  name="ParseMostActiveUsersParams",
  description="Set the parameters channel_url and channel to run the most active users tools.",
  func=parse_most_active_users
)
