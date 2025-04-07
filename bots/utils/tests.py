import os
from bots.agent import invoke_agent
from bots.state import State
from bots.tool_input import ToolInput
from bots.data.app import get_bot_character

bot_id = int(os.getenv('TEST_BOT'))

def make_tool_input(params={}):
  mock = {'id': bot_id}
  mock.update(params)
  state = State()
  state.character = get_bot_character(bot_id)
  state.tools_log = [('Mock', mock)]
  tool_input = ToolInput(state)
  return tool_input

def run_agent(test_id, mode, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, channel=None, user=None, blueprint=None):
  state = invoke_agent(
    run_name=test_id, 
    mode=mode,
    bot_id=bot_id, 
    request=request, 
    fid_origin=fid_origin, 
    parent_hash=parent_hash, 
    attachment_hash=attachment_hash, 
    root_parent_url=root_parent_url, 
    channel=channel, 
    user=user,
    blueprint=blueprint
  )
  state.debug()
  return state

