from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestPsycho(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'Psycho')
    self.assertEqual(len(bot.state.casts), 3)
    self.assertTrue(bot.state.reply)
    
  def test1(self):
    request = "Psycho analyze @randombishop"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], 253232)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    
  def test2(self):
    request = "psycho analyze me"
    fid_origin = 253232
    bot = run_bot(request, fid_origin=fid_origin)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], fid_origin)
    self.assertEqual(bot.state.action_params['user_name'], 'randombishop')
    
  def test3(self):
    request = "Psycho analyze @aethernet"
    bot = run_bot(request)
    self.assert_expected_output(bot)
    self.assertEqual(bot.state.action_params['fid'], 862185)
    self.assertEqual(bot.state.action_params['user_name'], 'aethernet')