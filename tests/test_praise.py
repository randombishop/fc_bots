from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestPraise(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'Praise')
    self.assertEqual(len(bot.state.casts), 3)
    self.assertTrue(bot.state.reply)
    
  def test1(self):
    request = "Praise @randombishop"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], 253232)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    
  def test2(self):
    request = "Praise me"
    fid_origin = 2
    bot = run_bot(request, fid_origin=fid_origin)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], fid_origin)
    self.assertEqual(bot.state.action_params['user_name'], 'v')
    
  def test3(self):
    request = "Praise a random user"
    bot = run_bot(request)
    self.assert_expected_output(bot)
