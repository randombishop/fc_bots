from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestSaySomethingInChannel(unittest.TestCase):

  def assert_expected_output(self, bot):
    self.assertEqual(bot.state.selected_action, 'SaySomethingInChannel')
    self.assertGreaterEqual(len(bot.state.casts), 1)
    
  def test1(self):
    root_parent_url = "chain://eip155:7777777/erc721:0xf7ebaea271e84a0c40e90bc6f5889dbfa0a12366"
    selected_action = "SaySomethingInChannel"
    bot = run_bot(root_parent_url=root_parent_url, selected_action=selected_action)
    self.assert_expected_output(bot)
    
  def test2(self):
    root_parent_url = "https://warpcast.com/~/channel/objkt"
    selected_action = "SaySomethingInChannel"
    bot = run_bot(root_parent_url=root_parent_url, selected_action=selected_action)
    self.assert_expected_output(bot)

  