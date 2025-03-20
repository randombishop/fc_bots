from langchain.agents import Tool
from bots.data.channels import get_channel_url
from bots.tools.autoprompt.summary_prompt_in_channel import summary_prompt_in_channel
from bots.tools.autoprompt.summary_prompt_no_channel import summary_prompt_no_channel


def auto_prompt_digest_casts(input):
  state = input.state
  channel_url = get_channel_url(state.selected_channel)
  prompt, params, log = None, None, ''
  if channel_url is None:
    prompt, params, log = summary_prompt_no_channel(state)
  else:
    prompt, params, log = summary_prompt_in_channel(state)
  state.action_params = params
  state.request = prompt
  state.conversation = state.request
  return {'action_params': params, 'request': prompt, 'conversation': state.request, 'log': log}
  

AutoPromptDigestCasts = Tool(
  name="autoprompt_digest_casts",
  description="Create an automatic prompt for the digest_casts action",
  func=auto_prompt_digest_casts
)