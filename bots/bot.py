import json
from langchain.agents import BaseSingleActionAgent
from langchain.schema import AgentAction, AgentFinish
from bots.utils.llms2 import get_llm, get_llm_img
from bots.data.app import get_bot_character
from bots.state import State
from bots.tool_input import ToolInput
from bots.tools import TOOL_DEPENDENCIES, TOOL_LIST
from bots.tools.memory import MEMORY_TOOLS



class Bot(BaseSingleActionAgent):
            
  def __init__(self):
    super().__init__()
    self._tools = TOOL_LIST
    self._llm = get_llm()
    self._llm_img = get_llm_img()
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
    input = ToolInput(
      state=self._state, 
      llm=self._llm, 
      llm_img=self._llm_img
    )
    return {"input":input}
  
  def todo(self, tool, done_steps=[]):
    if tool in TOOL_DEPENDENCIES:
      for dependency in TOOL_DEPENDENCIES[tool]:
        self.todo(dependency, done_steps)
    if tool not in self._todo and tool not in done_steps:
      self._todo.append(tool)
  
  def plan(self, intermediate_steps, callbacks, **kwargs):
    done_steps = [x[0].tool for x in intermediate_steps]
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
        self.todo('select_action_from_conversation', done_steps)
      elif self._state.selected_action_mode == 'channel':
        self.todo('select_action_for_channel', done_steps)
      elif self._state.selected_action_mode == 'main_feed':
        self.todo('select_action_for_main_feed', done_steps)
      return self.plan(intermediate_steps, callbacks, **kwargs)
    elif (self._state.selected_action is not None) and (self._state.action_tries == 0):
      self._state.action_tries += 1
      self.todo(self._state.selected_action, done_steps)
      return self.plan(intermediate_steps, callbacks, **kwargs)
    elif (self._state.casts is not None) and (not self._state.think_steps):
      self.todo('Like', done_steps)
      self.todo('Reply', done_steps)
      self.todo('Shorten', done_steps)
      self._state.think_steps = True
      return self.plan(intermediate_steps, callbacks, **kwargs)
    elif (not self._state.memory_steps):
      for m in MEMORY_TOOLS:
        self.todo(m.name, done_steps)
      self._state.memory_steps = True
      return self.plan(intermediate_steps, callbacks, **kwargs)
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
    
  async def aplan(self, intermediate_steps, **kwargs):
    return self.plan(intermediate_steps, **kwargs)


