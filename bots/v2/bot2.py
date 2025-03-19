import json
from langchain.agents import Tool, BaseSingleActionAgent
from langchain_google_vertexai import ChatVertexAI
from langchain.schema import AgentAction, AgentFinish
from bots.data.app import get_bot_character
from bots.v2.state import State
# Wakeup tools
from bots.v2.tools.wakeup.get_bio import GetBio
from bots.v2.tools.wakeup.get_conversation import GetConversation
from bots.v2.tools.wakeup.get_lore import GetLore
from bots.v2.tools.wakeup.get_style import GetStyle
from bots.v2.tools.wakeup.get_time import GetTime
# Fetch tools
from bots.v2.tools.fetch.get_bot_casts import GetBotCasts
from bots.v2.tools.fetch.get_channel_list import GetChannelList
from bots.v2.tools.fetch.get_trending import GetTrending
# Plan tools
from bots.v2.tools.plan.next import Next
from bots.v2.tools.plan.select_channel import SelectChannel
from bots.v2.tools.plan.select_action_mode import SelectActionMode
from bots.v2.tools.plan.select_action_from_conversation import SelectActionFromConversation
from bots.v2.tools.plan.select_action_for_channel import SelectActionForChannel
from bots.v2.tools.plan.select_action_for_main_feed import SelectActionForMainFeed

TOOL_BOX = [
  GetBio, GetConversation, GetLore, GetStyle, GetTime, 
  GetBotCasts, GetChannelList, GetTrending, 
  Next, SelectChannel, SelectActionMode, SelectActionFromConversation, SelectActionForChannel, SelectActionForMainFeed
]

TOOL_DEPENDENCIES = {
  x.name: x.metadata['depends_on'] for x in TOOL_BOX if x.metadata is not None and'depends_on' in x.metadata
}
   
class Bot2(BaseSingleActionAgent):
            
  def __init__(self):
    super().__init__()
    self._tools = TOOL_BOX
    self._llm = ChatVertexAI(model="gemini-1.5-pro")
    self._state = None
    self._todo = []
    
  @property
  def input_keys(self):
    return ["input"]
  
  def initialize_state(self, input):
    id = input['bot_id']
    character = get_bot_character(id)
    request = input['request'] if 'request' in input else None
    fid_origin = input['fid_origin'] if 'fid_origin' in input else None
    parent_hash = input['parent_hash'] if 'parent_hash' in input else None
    attachment_hash = input['attachment_hash'] if 'attachment_hash' in input else None
    root_parent_url = input['root_parent_url'] if 'root_parent_url' in input else None
    user = input['user'] if 'user' in input else None
    self._state = State(id=id, 
                        name=character['name'], 
                        character=character, 
                        request=request, 
                        fid_origin=fid_origin, 
                        parent_hash=parent_hash, 
                        attachment_hash=attachment_hash, 
                        root_parent_url=root_parent_url, 
                        user=user)
    self.todo('get_bio')
    self.todo('get_lore')
    self.todo('get_style')
    self.todo('get_time')
    self.todo('get_conversation')
    if self._state.request is None:
      self.todo('select_channel')
    self.todo('select_action_mode')
    
  def todo(self, tool):
    if tool in TOOL_DEPENDENCIES:
      for dependency in TOOL_DEPENDENCIES[tool]:
        self.todo(dependency)
    self._todo.append(tool)
  
  def next(self):
    return AgentAction(
      tool='_',
      tool_input={"state": self._state},
      log='')    

  def plan(self, intermediate_steps, callbacks, **kwargs):
    if self._state is None:
      input = json.loads(kwargs['input'])
      self.initialize_state(input)
    if len(self._todo) > 0: 
      tool = self._todo.pop(0)
      return AgentAction(
        tool=tool,
        tool_input={"state": self._state},
        log=tool)
    elif self._state.selected_action_mode is not None and self._state.selected_action is None and self._state.selected_action_tries == 0:
      self._state.selected_action_tries += 1
      if self._state.selected_action_mode == 'conversation':
        self.todo('select_action_from_conversation')
      elif self._state.selected_action_mode == 'channel':
        self.todo('select_action_for_channel')
      elif self._state.selected_action_mode == 'main_feed':
        self.todo('select_action_for_main_feed')
      return self.next()
    elif self._state.selected_action is not None and self._state.action_tries == 0:
      self._state.action_tries += 1
      self.todo(self._state.selected_action)
      return self.next()
    else:
      return AgentFinish(return_values={"output": self._state.log}, log='done')
    
  async def aplan(self, intermediate_steps, **kwargs):
    return self.plan(intermediate_steps, **kwargs)


