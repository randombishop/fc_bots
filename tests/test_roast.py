from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot

class TestRoast(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.selected_action, 'Roast')
    self.assertEqual(len(state.casts), 1)
    self.assertTrue(state.reply)
    
  def test1(self):
    request = "Roast randombishop"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['fid'], 253232)
    self.assertEqual(state.action_params['user_name'], 'randombishop')
    
  def test2(self):
    request = "roast me"
    fid_origin = 253232
    state = run_bot(request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['fid'], fid_origin)
    self.assertEqual(state.action_params['user_name'], 'randombishop')
