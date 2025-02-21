from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestSelectAction(unittest.TestCase):
  
  def test1(self):
    bot = run_bot(selected_channel='nature')
    self.assertIsNotNone(bot.state.selected_action)
    
  def test2(self):
    bot = run_bot(selected_channel='None')
    self.assertIsNotNone(bot.state.selected_action)
    
  