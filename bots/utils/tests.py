import os
from bots.agent import invoke_agent
from bots.state import State
from bots.tool_input import ToolInput
from bots.utils.llms2 import get_llm, get_llm_img
from bots.assistant import Assistant
from bots.bot import Bot

bot_id = int(os.getenv('TEST_BOT'))

def make_tool_input():
  state = State({'bot_id': bot_id})
  tool_input = ToolInput(state, get_llm(), get_llm_img())
  return tool_input

def run_agent(agent_class, test_id, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, channel=None, user=None, blueprint=None):
  agent_classes = {
    'assistant': Assistant,
    'bot': Bot
  }
  agent_class = agent_classes[agent_class]
  state = invoke_agent(
    agent_class=agent_class,
    run_name=test_id, 
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

