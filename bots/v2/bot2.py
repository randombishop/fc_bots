from langchain.agents import Tool, BaseSingleActionAgent
from langchain_google_vertexai import ChatVertexAI
from langchain.schema import AgentAction, AgentFinish
from bots.data.app import get_bot_character
from bots.v2.state import State
# Wakeup tools
from bots.v2.tools.wakeup.get_bio import GetBio
from bots.v2.tools.wakeup.get_lore import GetLore
from bots.v2.tools.wakeup.get_style import GetStyle
from bots.v2.tools.wakeup.get_time import GetTime
# Fetch tools
from bots.v2.tools.fetch.get_trending import GetTrending
from bots.v2.tools.fetch.get_bot_casts import GetBotCasts
# Plan tools
from bots.v2.tools.plan.select_channel import SelectChannel

TOOL_BOX = [
  GetBio, GetLore, GetStyle, GetTime, 
  GetTrending, GetBotCasts, 
  SelectChannel
]

TOOL_DEPENDENCIES = {
  x.name: x.metadata['depends_on'] for x in TOOL_BOX if 'depends_on' in x.metadata
}
   
class Bot2(BaseSingleActionAgent):
            
  def __init__(self, id):
    super().__init__()
    character = get_bot_character(id)
    self._tools = TOOLBOX
    self._llm = ChatVertexAI(model="gemini-1.5-pro")
    self._state = State(id=id, name=character['name'], character=character)
    self._todo = []
    self.todo('get_bio')
    self.todo('get_lore')
    self.todo('get_style')
    self.todo('get_time')
    self.todo('select_channel')
    
  @property
  def input_keys(self):
    return ["input"]

  def todo(self, tool):
    if tool in TOOL_DEPENDENCIES:
      for dependency in TOOL_DEPENDENCIES[tool]:
        self._todo.append(dependency)
    self._todo.append(tool)
    
  def plan(self, intermediate_steps, callbacks, **kwargs):
    if len(self._todo) > 0: 
      tool = self._todo.pop(0)
      return AgentAction(
        tool=tool,
        tool_input={"state": self._state},
        log=tool)
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
    
  async def aplan(self, intermediate_steps, **kwargs):
    return self.plan(intermediate_steps, **kwargs)


