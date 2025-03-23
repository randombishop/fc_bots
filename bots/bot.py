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
    self._todo = None
    
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
  
  def initialize(self, input):
    self._state = State(input)
    self._todo = [
      'BotWakeup',
      'BotPlan',
      'BotParse',
      'BotFetch',
      'BotPrepare',
      'BotCompose',
      'BotCheck',
      'BotMemorize'
    ]
      
  def plan(self, intermediate_steps, callbacks, **kwargs):
    if self._state is None:
      input = json.loads(kwargs['input'])
      self.initialize(input)
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
