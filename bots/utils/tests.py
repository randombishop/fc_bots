import os
from bots.bot import Bot, generate_bot_response
from bots.bot_state import BotState
from bots.data.app import get_bot_character


bot_id = int(os.getenv('TEST_BOT'))

def make_state():
  state = BotState(id=bot_id)
  return state

def make_character():
  character = get_bot_character(bot_id)
  return character

def make_bot():
  bot_character = make_character()
  bot = Bot(bot_id, bot_character)
  return bot

def make_character_and_state(request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None):  
  character = make_character()
  state = BotState(id=bot_id)
  state.request = request
  state.fid_origin = fid_origin
  state.parent_hash = parent_hash
  state.attachment_hash = attachment_hash
  state.root_parent_url = root_parent_url
  return character, state

def run_bot(request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, selected_channel=None, selected_action=None):
  return generate_bot_response(bot_id, request, fid_origin=fid_origin, parent_hash=parent_hash, attachment_hash=attachment_hash, 
                  root_parent_url=root_parent_url, 
                  selected_channel=selected_channel, selected_action=selected_action,
                  debug=True)
