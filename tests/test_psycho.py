from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestPsycho(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.get('intent'), 'Psycho')
    self.assertTrue(state.get('valid'))
    
  def test1(self):
    request = "Psycho analyze @randombishop"
    state = run_agent(test_id='TestPsycho:1', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user_fid'), 253232)
    self.assertEqual(state.get('user'), 'randombishop')
    
  def test2(self):
    request = "psycho analyze me"
    fid_origin = 253232
    state = run_agent(test_id='TestPsycho:2', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user_fid'), fid_origin)
    self.assertEqual(state.get('user'), 'randombishop')
    
  def test3(self):
    request = "Psycho analyze @aethernet"
    state = run_agent(test_id='TestPsycho:3', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user_fid'), 862185)
    self.assertEqual(state.get('user'), 'aethernet')