import json
from langchain.agents import BaseSingleActionAgent
from langchain_google_vertexai import ChatVertexAI
from langchain.schema import AgentAction, AgentFinish
from bots.data.app import get_bot_character
from bots.v2.state import State
from bots.v2.tools import TOOL_DEPENDENCIES, TOOL_LIST


class Bot2(BaseSingleActionAgent):
            
  def __init__(self):
    super().__init__()
    self._tools = TOOL_LIST
    self._llm = ChatVertexAI(model="gemini-1.5-flash-002")
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
    if self._state.request is None:
      self.todo('select_channel')
    self.todo('select_action_mode')
    
  def get_tool_input(self):
    return {"input":{"state": self._state, "llm": self._llm}}
  
  def todo(self, tool):
    if tool in TOOL_DEPENDENCIES:
      for dependency in TOOL_DEPENDENCIES[tool]:
        self.todo(dependency)
    self._todo.append(tool)
  
  def next(self):
    return AgentAction(
      tool='_', 
      tool_input=self.get_tool_input(), 
      log='')    

  def plan(self, intermediate_steps, callbacks, **kwargs):
    if self._state is None:
      input = json.loads(kwargs['input'])
      self.initialize_state(input)
    if len(self._todo) > 0: 
      tool = self._todo.pop(0)
      return AgentAction(
        tool=tool,
        tool_input=self.get_tool_input(),
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


