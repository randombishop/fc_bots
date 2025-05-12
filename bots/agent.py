import json
from langchain.agents import BaseSingleActionAgent
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentExecutor
from bots.tools import TOOLS
from bots.state import State


class Agent(BaseSingleActionAgent):
            
  def __init__(self):
    super().__init__()
    self._tools = TOOLS
    self._state = None
    
  @property
  def input_keys(self):
    return ["input"]
  
  def next_phase(self):
    if not self._state.should_continue:
      return AgentFinish(return_values={"output": self._state}, log='done')
    elif self._state.iterations != 'done':
      if self._state.mode == 'bot':
        return AgentAction(
          tool='intent',
          tool_input={'state': self._state},
          log='')
      elif self._state.mode == 'assistant':
        return AgentAction(
          tool='plan',
          tool_input={'state': self._state},
          log='')
    elif not self._state.composed:
      return AgentAction(
        tool='compose',
        tool_input={'state': self._state},
        log='')
    elif (not self._state.checked) and (self._state.casts is not None) and (len(self._state.casts) > 0):
      return AgentAction(
        tool='check',
        tool_input={'state': self._state},
        log='')
    elif not self._state.memorized:
      return AgentAction(
        tool='memorize',
        tool_input={'state': self._state},
        log='')
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
    
  def next_action(self, intermediate_steps, callbacks, **kwargs):
    if not self._state.should_continue:
      return AgentFinish(return_values={"output": self._state}, log='done')
    elif self._state.todo is not None and len(self._state.todo) > 0:
      tool_config = self._state.todo.pop(0)
      input = {
        'state': self._state,
        'config': tool_config
      }
      return AgentAction(
        tool=tool_config['tool'],
        tool_input={'input': input},
        log='')
    elif self._state.mode in ['bot', 'assistant']:
      return self.next_phase()
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
    
  def plan(self, intermediate_steps, callbacks, **kwargs):
    if self._state is None:
      self._state = State()
      input = json.loads(kwargs['input'])
      input['state'] = self._state
      return AgentAction(
        tool='init_state',
        tool_input={'input': input},
        log='')
    else:
      return self.next_action(intermediate_steps, callbacks, **kwargs)
    
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
