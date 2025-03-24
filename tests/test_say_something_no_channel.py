from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestSaySomethingNoChannel(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'SaySomethingNoChannel')
    self.assertGreaterEqual(len(state.casts), 1)
    
  def test1(self):
    action = "SaySomethingNoChannel"
    state = run_bot(action=action)
    self.assert_expected_output(state)
    
  
  