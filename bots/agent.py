import json
from langchain.agents import BaseSingleActionAgent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentExecutor
from bots.utils.llms2 import get_llm, get_llm_img
from bots.state import State
from bots.tool_input import ToolInput
from bots.tools import TOOL_LIST


class Agent(BaseSingleActionAgent):
            
  def __init__(self):
    super().__init__()
    self._tools = TOOL_LIST
    self._llm = get_llm()
    self._llm_img = get_llm_img()
    self._state = None
    
  @property
  def input_keys(self):
    return ["input"]
  
  def get_tool_input(self):
    input = ToolInput(
      state=self._state, 
      llm=self._llm, 
      llm_img=self._llm_img
    )
    return {"input":input}
  
  def next_phase(self):
    if self._state.get('parsed') is None:
      return AgentAction(
        tool='Parse',
        tool_input=self.get_tool_input(),
        log='')
    elif self._state.get('fetched') is None:
      return AgentAction(
        tool='Fetch',
        tool_input=self.get_tool_input(),
        log='')
    elif self._state.get('prepared') is None:
      return AgentAction(
        tool='Prepare',
        tool_input=self.get_tool_input(),
        log='')
    elif self._state.get('composed') is None:
      return AgentAction(
        tool='ComposeMulti',
        tool_input=self.get_tool_input(),
        log='')
    elif (not self._state.get('checked')) and (self._state.get('casts') is not None) and (len(self._state.get('casts')) > 0):
      return AgentAction(
        tool='Check',
        tool_input=self.get_tool_input(),
        log='')
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
  
  def next_action(self):
    if self._state.get('todo') is not None and len(self._state.get('todo')) > 0:
      return AgentAction(
        tool=self._state.get('todo').pop(0),
        tool_input=self.get_tool_input(),
        log='')
    elif self._state.get('mode') in ['bot', 'assistant']:
      return self.next_phase()
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
  
  def plan(self, intermediate_steps, callbacks, **kwargs):
    if self._state is None:
      self._state = State()
      input = json.loads(kwargs['input'])
      input['state'] = self._state
      return AgentAction(
        tool='InitState',
        tool_input={'input': input},
        log='')
    self._state.tools_log = intermediate_steps
    return self.next_action()
    
  async def aplan(self, intermediate_steps, **kwargs):
    return self.plan(intermediate_steps, **kwargs)



def invoke_agent(run_name, mode, bot_id, 
                 request=None, 
                 fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, 
                 channel=None, user=None,
                 blueprint=None):
  input = {
      'bot_id': bot_id,
      'mode': mode,
      'request': request,
      'fid_origin': fid_origin,
      'parent_hash': parent_hash,
      'attachment_hash': attachment_hash,
      'root_parent_url': root_parent_url,
      'channel': channel,
      'blueprint': blueprint,
      'user': user
  }
  assistant = Agent()
  executor = AgentExecutor(agent=assistant, tools=assistant._tools, max_iterations=25)
  result = executor.invoke(input=json.dumps(input), config={"run_name": run_name})
  if 'output' not in result:
    raise Exception(f"Assistant {bot_id} returned no output")
  if 'error' in result:
    raise Exception(f"Assistant {bot_id} returned an error: {result['error']}")
  output = result['output']
  if not isinstance(output, State):
    raise Exception(f"Assistant {bot_id} returned an unexpected output: {output}")
  return output
