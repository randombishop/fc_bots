from langchain.agents import Tool
from bots.tools.wakeup.get_bio import GetBio
from bots.tools.wakeup.get_lore import GetLore
from bots.tools.wakeup.get_style import GetStyle
from bots.tools.wakeup.get_time import GetTime


def assistant_wakeup(input):
  GetBio.invoke({'input': input})
  GetLore.invoke({'input': input})
  GetStyle.invoke({'input': input})
  GetTime.invoke({'input': input})
  return {'log': 'ok'}


AssistantWakeup = Tool(
  name="AssistantWakeup",
  description="Assistant wakeup phase",
  func=assistant_wakeup
)