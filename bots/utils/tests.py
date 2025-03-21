import os
from bots.bot import invoke_bot
from bots.assistant import invoke_assistant


bot_id = int(os.getenv('TEST_BOT'))


def run_bot(test_id, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, selected_channel=None, selected_action=None):
  state = invoke_bot(
    run_name=test_id, 
    bot_id=bot_id, 
    request=request, 
    fid_origin=fid_origin, 
    parent_hash=parent_hash, 
    attachment_hash=attachment_hash, 
    root_parent_url=root_parent_url, 
    selected_channel=selected_channel, 
    selected_action=selected_action
  )
  state.debug()
  return state

def run_assistant(test_id, instructions):
  state = invoke_assistant(
    run_name=test_id, 
    bot_id=bot_id, 
    instructions=instructions
  )
  state.debug()
  return state