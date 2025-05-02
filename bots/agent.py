import json
from langchain.agents import BaseSingleActionAgent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentExecutor
from bots.state import State
from bots.tools.plan.init import InitState

class Agent(BaseSingleActionAgent):
            
  def __init__(self):
    super().__init__()
    self._tools = [InitState]
    self._state = None
    
  @property
  def input_keys(self):
    return ["input"]
  
  def plan(self, intermediate_steps, callbacks, **kwargs):
    if self._state is None:
      self._state = State()
      input = json.loads(kwargs['input'])
      input['state'] = self._state
      return AgentAction(
        tool='InitState',
        tool_input={'input': input},
        log='')
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
    
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
      'user': user,
      'blueprint': blueprint
  }
  run_name = f'{run_name}/{mode}/{bot_id}'
  tags = []
  if blueprint is not None:
    tags.append('blueprint:'+str(blueprint))
  if channel is not None:
    tags.append('channel:'+str(channel))
  if user is not None:
    tags.append('user:'+str(user))
  if fid_origin is not None:
    tags.append('fid_origin:'+str(fid_origin))
  agent = Agent()
  executor = AgentExecutor(agent=agent, tools=agent._tools, max_iterations=25)
  result = executor.invoke(input=json.dumps(input), config={"run_name": run_name, "tags": tags})
  if 'output' not in result:
    raise Exception(f"Assistant {bot_id} returned no output")
  if 'error' in result:
    raise Exception(f"Assistant {bot_id} returned an error: {result['error']}")
  output = result['output']
  if not isinstance(output, State):
    raise Exception(f"Assistant {bot_id} returned an unexpected output: {output}")
  return output
