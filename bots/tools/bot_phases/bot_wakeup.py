from langchain.agents import Tool
from bots.tools.wakeup.get_bio import GetBio
from bots.tools.wakeup.get_lore import GetLore
from bots.tools.wakeup.get_style import GetStyle
from bots.tools.wakeup.get_time import GetTime
from bots.tools.wakeup.get_conversation import GetConversation


def bot_wakeup(input):
  GetBio.invoke({'input': input})
  GetLore.invoke({'input': input})
  GetStyle.invoke({'input': input})
  GetTime.invoke({'input': input})
  GetConversation.invoke({'input': input})
  return {'log': 'ok'}


BotWakeup = Tool(
  name="BotWakeup",
  description="Bot wakeup phase",
  func=bot_wakeup
)