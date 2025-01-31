import unittest
from bots.utils.tests import make_bot
from bots.bot import Bot


class TestBot(unittest.TestCase):
  
  def test1(self):
    bot = make_bot()
    # Check that bot has some data
    self.assertIsInstance(bot.character['name'], str)
    self.assertIsInstance(bot.character['bio'], list)
    self.assertIsInstance(bot.character['lore'], list)
    self.assertIsInstance(bot.character['style'], list)
    # Test chat
    request = "Who are you?"
    bot.respond(request)
    print(bot.state.format())
    
