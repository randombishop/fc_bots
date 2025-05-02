import os
from bots.agent import invoke_agent


bot_id = int(os.getenv('TEST_BOT'))


def debug(state):
  print("-"*32)
  variables = '\n'.join([str(v) for v in state.variables.values()])
  print(f"#VARIABLES\n{variables}")
  print("-"*32)
  

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
  debug(state)
  return state

