from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestSelectAction(unittest.TestCase):
  
  def test1(self):
    state = run_bot(selected_channel='nature')
    self.assertIsNotNone(state.selected_action)
    
  def test2(self):
    state = run_bot(selected_channel='None')
    self.assertIsNotNone(state.selected_action)
    
  