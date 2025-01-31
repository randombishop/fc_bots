import os
from bots.bot import Bot
from bots.bot_state import BotState
from bots.data.app import get_bot_character


def make_character():
  character = get_bot_character(os.getenv('TEST_BOT'))
  return character

def make_bot():
  bot_character = make_character()
  bot = Bot(bot_character)
  return bot

def make_character_and_state(request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None):  
  character = make_character()
  state = BotState()
  state.request = request
  state.fid_origin = fid_origin
  state.parent_hash = parent_hash
  state.attachment_hash = attachment_hash
  state.root_parent_url = root_parent_url
  return character, state