from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestPraise(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.get('intent'), 'Praise')
    self.assertTrue(state.get('valid'))
    
  def test1(self):
    request = "Praise @randombishop"
    state = run_agent(test_id='TestPraise:1', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user_fid'), 253232)
    self.assertEqual(state.get('user'), 'randombishop')
    
  def test2(self):
    request = "Praise me"
    fid_origin = 253232
    state = run_agent(test_id='TestPraise:2', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user_fid'), fid_origin)
    self.assertEqual(state.get('user'), 'randombishop')
    
  def test3(self):
    request = "Praise a random user"
    state = run_agent(test_id='TestPraise:3', mode='bot', request=request)
    self.assert_expected_output(state)
