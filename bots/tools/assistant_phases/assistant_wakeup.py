from langchain.agents import Tool
from bots.tools.wakeup.get_bio import GetBio
from bots.tools.wakeup.get_lore import GetLore
from bots.tools.wakeup.get_style import GetStyle
from bots.tools.wakeup.get_time import GetTime

def wakeup(input):
  ans = {}
  bio = GetBio.invoke({'input': input})
  ans.update(bio)
  lore = GetLore.invoke({'input': input})
  ans.update(lore)
  style = GetStyle.invoke({'input': input})
  ans.update(style)
  time = GetTime.invoke({'input': input})
  ans.update(time)
  state = input.state
  state.wokeup = True
  return ans
    

AssistantWakeup = Tool(
  name="AssistantWakeup",
  description="Assistant wakeup phase",
  metadata={
    'outputs': ['bio', 'lore', 'style', 'time']
  },
  func=wakeup
)