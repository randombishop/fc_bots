import os
from bots.bot import invoke_bot
from bots.assistant import invoke_assistant
from bots.state import State
from bots.tool_input import ToolInput
from bots.utils.llms2 import get_llm, get_llm_img

bot_id = int(os.getenv('TEST_BOT'))

def make_tool_input():
  state = State({'bot_id': bot_id})
  tool_input = ToolInput(state, get_llm(), get_llm_img())
  return tool_input

def run_bot(test_id, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, channel=None, action=None, user=None):
  state = invoke_bot(
    run_name=test_id, 
    bot_id=bot_id, 
    request=request, 
    fid_origin=fid_origin, 
    parent_hash=parent_hash, 
    attachment_hash=attachment_hash, 
    root_parent_url=root_parent_url, 
    channel=channel, 
    action=action,
    user=user
  )
  state.debug()
  return state

def run_assistant(test_id, request=None, channel=None):
  state = invoke_assistant(
    run_name=test_id, 
    bot_id=bot_id, 
    request=request,
    channel=channel
  )
  state.debug()
  return state