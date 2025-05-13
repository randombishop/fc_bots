from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent

class TestRoast(unittest.TestCase):

  def assert_expected_output(self, state, fid, username):
    self.assertEqual(state.plan['intent'], 'Roast')
    self.assertTrue(state.valid)
    user_id = state.get_variable_values('UserId')[-1]
    self.assertEqual(user_id.fid, fid)
    self.assertEqual(user_id.username, username)
    
  def test1(self):
    request = "Roast randombishop"
    state = run_agent(test_id='TestRoast:1', mode='bot', request=request)
    self.assert_expected_output(state, 253232, 'randombishop')
    
  def test2(self):
    request = "roast me"
    fid_origin = 253232
    state = run_agent(test_id='TestRoast:2', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state, fid_origin, 'randombishop')
