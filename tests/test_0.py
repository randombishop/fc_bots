import unittest
from bots.utils.tests import make_bot
from bots.bot import Bot


class Test0(unittest.TestCase):
  
  def test1(self):
    bot = make_bot()
    # Check that bot has some data
    self.assertIsInstance(bot.character['name'], str)
    self.assertIsInstance(bot.character['bio'], list)
    self.assertIsInstance(bot.character['lore'], list)
    self.assertIsInstance(bot.character['style'], list)
    bot.initialize()
    bot.wakeup()
    print(bot.state.format())
    
