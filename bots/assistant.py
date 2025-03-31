import json
from bots.agent import Agent
from langchain.schema import AgentAction, AgentFinish


class Assistant(Agent):
            
  def __init__(self):
    super().__init__()

  def next_action(self):
    if not self._state.get('wokeup'):
      return AgentAction(
        tool='WakeupAssistant',
        tool_input=self.get_tool_input(),
        log='')
    elif self._state.get('todo') is not None and len(self._state.get('todo')) > 0:
      return AgentAction(
        tool=self._state.get('todo').pop(0),
        tool_input=self.get_tool_input(),
        log='')
    elif self._state.get('parse_tools') is None:
      return AgentAction(
        tool='Parse',
        tool_input=self.get_tool_input(),
        log='')
    elif self._state.get('fetch_tools') is None:
      return AgentAction(
        tool='Fetch',
        tool_input=self.get_tool_input(),
        log='')
    elif self._state.get('prepare_tools') is None:
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
        tool='CheckAssistant',
        tool_input=self.get_tool_input(),
        log='')
    else:
      return AgentFinish(return_values={"output": self._state}, log='done')
    
  