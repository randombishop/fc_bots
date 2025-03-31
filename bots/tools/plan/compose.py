from langchain.agents import Tool
from bots.tools.compose.compose_one import ComposeOne
from bots.tools.compose.compose_multi import ComposeMulti


def check(input):
  state = input.state
  ans = {'composed': True}
  mode = state.get('mode')
  if mode == 'bot':
    compose = ComposeOne.invoke({'input': input})
    ans.update(compose)
  elif mode == 'assistant':
    compose = ComposeMulti.invoke({'input': input})
    ans.update(compose)
  return ans
    

Compose = Tool(
  name="Compose",
  description="Compose outputs phase",
  func=check
)