from langchain.agents import Tool
from bots.tools.autoprompt.perplexity_question_in_channel import perplexity_question_in_channel
from bots.tools.autoprompt.perplexity_question_no_channel import perplexity_question_no_channel



def auto_prompt_perplexity(input):
  state = input.state
  channel = state.selected_channel
  question, log = None, None
  if channel is None or channel in ['', 'None']:
    question, log = perplexity_question_no_channel(state)
  else:
    question, log = perplexity_question_in_channel(state)
  state.action_params = {'question': question}
  state.request = f'Ask Perplexity {question}'
  state.conversation = state.request
  return {
    'action_params': state.action_params,
    'request': state.request,
    'conversation': state.conversation,
    'log': log
  }
    
AutoPromptPerplexity = Tool(
  name="auto_prompt_perplexity",
  description="Create an automatic prompt for the perplexity action",
  func=auto_prompt_perplexity
)
