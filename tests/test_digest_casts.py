from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestDigestCasts(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'Summary')
    self.assertGreaterEqual(len(state.casts), 1)
    self.assertTrue(state.reply)
      
  def test1(self):
    request = "Give me a summary using keyword ethereum"
    state = run_bot(test_id='TestDigestCasts:test1', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['keyword'], 'ethereum')
    
  def test2(self):
    request = "Summary for arts category"
    state = run_bot(test_id='TestDigestCasts:test2', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['category'], 'c_arts')
    
  def test3(self):
    request = "Summary for /rodeo channel?"
    state = run_bot(test_id='TestDigestCasts:test3', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['channel'], 'https://warpcast.com/~/channel/rodeo-club')
    
  def test4(self):
    request = "Summary of posts about the beauty of canadian landscapes"
    state = run_bot(test_id='TestDigestCasts:test4', request=request)
    self.assert_expected_output(state)
    self.assertIsNotNone(state.action_params['search'])
      
  def test5(self):
    request = "Summary of @randombishop's posts"
    state = run_bot(test_id='TestDigestCasts:test5', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['user_name'], 'randombishop')
