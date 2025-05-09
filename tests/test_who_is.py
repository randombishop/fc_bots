from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestWhoIs(unittest.TestCase):
  
  def assert_expected_output(self, state, fid, username):
    self.assertEqual(state.plan['intent'], 'WhoIs')
    user = state.get_variable_values('UserId')[-1]
    self.assertEqual(user.fid, fid)
    self.assertEqual(user.username, username)
    
  def test1(self):
    request = "Who is @randombishop?"
    state = run_agent(test_id='TestWhoIs:1', mode='bot', request=request)
    self.assert_expected_output(state, 253232, 'randombishop')

  def test2(self):
    request = "Who am I?"
    fid_origin = 253232
    state = run_agent(test_id='TestWhoIs:2', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state, fid_origin, 'randombishop')


    
