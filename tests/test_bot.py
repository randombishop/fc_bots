import unittest
import os
from bots.data.app import get_bot_character
from bots.bot import Bot


class TestBot(unittest.TestCase):
  
  def test1(self):
    fid_owner = os.getenv('TEST_BOT')
    print(fid_owner)
    bot_character = get_bot_character(fid_owner)
    bot = Bot(bot_character)
    # Check that bot has some data
    self.assertIsInstance(bot.character['name'], str)
    self.assertIsInstance(bot.character['bio'], list)
    self.assertIsInstance(bot.character['lore'], list)
    self.assertIsInstance(bot.character['style'], list)
    # Test chat
    request = "Who are you?"
    bot.respond(request)
    print(bot.state.format())
    self.assertEqual(bot.state.request, request)
