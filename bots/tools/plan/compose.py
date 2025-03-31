from langchain.agents import Tool
from bots.tools.compose.compose_bot_response import ComposeBotResponse
from bots.tools.compose.compose_assistant_response import ComposeAssistantResponse


def compose(input):
  state = input.state
  ans = {'composed': True}
  mode = state.get('mode')
  if mode == 'bot':
    compose = ComposeBotResponse.invoke({'input': input})
    ans.update(compose)
  elif mode == 'assistant':
    compose = ComposeAssistantResponse.invoke({'input': input})
    ans.update(compose)
  return ans
    

Compose = Tool(
  name="Compose",
  description="Compose outputs phase",
  func=compose
)