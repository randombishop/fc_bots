import json
from langchain.agents import BaseSingleActionAgent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentExecutor
from bots.utils.llms2 import get_llm, get_llm_img
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
    if not self._state.wokeup:
      return AgentAction(
        tool='WakeupAssistant',
        tool_input=self.get_tool_input(),
        log='')
    elif not self._state.parsed:
      return AgentAction(
        tool='Parse',
        tool_input=self.get_tool_input(),
        log='')
    elif not self._state.fetched:
      return AgentAction(
        tool='Fetch',
        tool_input=self.get_tool_input(),
        log='')
    elif not self._state.composed:
      return AgentAction(
        tool='ComposeMulti',
        tool_input=self.get_tool_input(),
        log='')
    elif (not self._state.checked) and (self._state.get('casts') is not None) and (len(self._state.get('casts')) > 0):
      return AgentAction(
        tool='CheckAssistant',
        tool_input=self.get_tool_input(),
        log='')
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
    
  async def aplan(self, intermediate_steps, **kwargs):
    return self.plan(intermediate_steps, **kwargs)



def invoke_assistant(run_name, bot_id, request=None, channel=None):
  input = {
      'bot_id': bot_id,
      'request': request,
      'channel': channel
  }
  assistant = Assistant()
  executor = AgentExecutor(agent=assistant, tools=assistant._tools, max_iterations=10)
  result = executor.invoke(input=json.dumps(input), config={"run_name": run_name})
  if 'output' not in result:
    raise Exception(f"Assistant {bot_id} returned no output")
  if 'error' in result:
    raise Exception(f"Assistant {bot_id} returned an error: {result['error']}")
  output = result['output']
  if not isinstance(output, State):
    raise Exception(f"Assistant {bot_id} returned an unexpected output: {output}")
  return output
