import json
from langchain.agents import BaseSingleActionAgent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentExecutor
from bots.utils.llms2 import get_llm, get_llm_img
from bots.data.app import get_bot_character
from bots.state import State
from bots.tool_input import ToolInput
from bots.tools import TOOL_LIST



class Assistant(BaseSingleActionAgent):
            
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
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
    
  async def aplan(self, intermediate_steps, **kwargs):
    return self.plan(intermediate_steps, **kwargs)



def invoke_assistant(run_name, bot_id, instructions):
  input = {
      'bot_id': bot_id,
      'instructions': instructions
  }
  assistant = Assistant()
  executor = AgentExecutor(agent=assistant, tools=assistant._tools, max_iterations=25)
  result = executor.invoke(input=json.dumps(input), config={"run_name": run_name})
  if 'output' not in result:
    raise Exception(f"Assistant {bot_id} returned no output")
  if 'error' in result:
    raise Exception(f"Assistant {bot_id} returned an error: {result['error']}")
  return result['output']
