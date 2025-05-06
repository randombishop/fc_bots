from langchain.agents import Tool
from bots.tools.intent.intent_assistant import IntentAssistant
from bots.tools.intent.intent_bot import IntentBot


def intent(input):
  state = input.state
  mode = state.get('mode')
  if mode == 'assistant':
    return IntentAssistant.invoke({'input': input})
  elif mode == 'bot':
    return IntentBot.invoke({'input': input})
  else:
    raise Exception(f"Invalid mode `{mode}`. should be assistant or bot")
  
Intent = Tool(
  name="Intent",
  description="Intent planning phase",
  func=intent
)