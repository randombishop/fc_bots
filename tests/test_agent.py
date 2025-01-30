import unittest
from bots.data.app import get_bot_character
import os

class TestAgent(unittest.TestCase):
  
  def test1(self):
    fid_owner = os.getenv('TEST_BOT')
    print(fid_owner)
    bot_character = get_bot_character(fid_owner)
    print(bot_character['name'])
