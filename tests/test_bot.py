import unittest
import os
from bots.data.app import get_bot_character
from bots.bot import Bot

class TestAgent(unittest.TestCase):
  
  def test1(self):
    fid_owner = os.getenv('TEST_BOT')
    print(fid_owner)
    bot_character = get_bot_character(fid_owner)
    bot = Bot(bot_character)
    print(bot.name)
    self.assertIsInstance(bot.name, str)
    self.assertIsInstance(bot.bio, list)
    self.assertIsInstance(bot.lore, list)
    self.assertIsInstance(bot.style, list)
