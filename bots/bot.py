import json
from langchain.agents import BaseSingleActionAgent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentExecutor
from bots.utils.llms2 import get_llm, get_llm_img
from bots.state import State
from bots.tool_input import ToolInput
from bots.tools import TOOL_LIST


class Bot(BaseSingleActionAgent):
            
  def __init__(self):
    super().__init__()
    self._tools = TOOL_LIST
    self._llm = get_llm()
    self._llm_img = get_llm_img()
    self._state = None
    self._wakeup = [
      'GetBio',
      'GetLore',
      'GetStyle',
      'GetTime',
      'GetConversation',
      'ShouldContinue'
    ]
    
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
        log='Initialization')
    self._state.tools_log = intermediate_steps
    if len(self._wakeup) > 0: 
      tool = self._wakeup.pop(0)
      return AgentAction(
        tool=tool,
        tool_input=self.get_tool_input(),
        log='Wakeup Step')
    elif not self._state.get('should_continue'):
      return AgentFinish(return_values={"output": self._state}, log='Should not continue the conversation')
    elif not self._state.tools_done:
      next_tool = self._state.next_tool
      if next_tool is not None:
        self._state.next_tool = None
        return AgentAction(
          tool=next_tool,
          tool_input=self.get_tool_input(),
          log='Tool')
      else:
        return AgentAction(
          tool='SelectTool',
          tool_input=self.get_tool_input(),
          log='Select'
        )
    elif not self._state.composed:
      self._state.composed = True
      return AgentAction(
        tool='ComposeCasts',
        tool_input=self.get_tool_input(),
        log='Compose')
    elif not self._state.checked and self._state.get('casts') is not None and len(self._state.get('casts')) > 0:
      self._state.checked = True
      return AgentAction(
        tool='AssistantCheck',
        tool_input=self.get_tool_input(),
        log='Check')
    else:
      return AgentFinish(return_values={"output": self._state}, log='Done')
    
  async def aplan(self, intermediate_steps, **kwargs):
    return self.plan(intermediate_steps, **kwargs)




def invoke_bot(run_name, bot_id, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, channel=None, action=None, user=None):
  input = {
      'bot_id': bot_id,
      'request': request,
      'fid_origin': fid_origin,
      'parent_hash': parent_hash,
      'attachment_hash': attachment_hash,
      'root_parent_url': root_parent_url,
      'channel': channel,
      'action': action,
      'user': user
  }
  bot = Bot()
  executor = AgentExecutor(agent=bot, tools=bot._tools, max_iterations=25)
  result = executor.invoke(input=json.dumps(input), config={"run_name": run_name})
  if 'output' not in result:
    raise Exception(f"Bot {bot_id} returned no output")
  if 'error' in result:
    raise Exception(f"Bot {bot_id} returned an error: {result['error']}")
  return result['output']
