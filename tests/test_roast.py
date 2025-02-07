from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_bot


class TestRoast(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'Roast')
    self.assertEqual(len(bot.state.casts), 1)
    self.assertTrue(bot.state.reply)
    
  def test1(self):
    request = "Roast randombishop"
    bot = make_bot()
    bot.respond(request)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], 253232)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    
  def test2(self):
    request = "roast me"
    fid_origin = 253232
    bot = make_bot()
    bot.respond(request, fid_origin=fid_origin)
    bot.state.debug_action()
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], fid_origin)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
