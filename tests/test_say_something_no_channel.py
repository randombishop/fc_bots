from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestSaySomethingNoChannel(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'SaySomethingNoChannel')
    self.assertGreaterEqual(len(bot.state.casts), 1)
    
  def test1(self):
    selected_action = "SaySomethingNoChannel"
    bot = run_bot(selected_action=selected_action)
    self.assert_expected_output(bot)
    
  
  