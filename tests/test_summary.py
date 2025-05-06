from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestSummary(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.plan['intent'], 'Summary')
    self.assertTrue(state.valid)
      
  def test1(self):
    request = "Give me a summary using keyword ethereum"
    state = run_agent(test_id='TestSummary:test1', mode='bot', request=request)
    self.assert_expected_output(state)
    keywords = [x.value.keyword for x in state.get_variables() if x.value.__class__.__name__=='Keyword']
    self.assertIn('ethereum', keywords)
    
  def test2(self):
    request = "Summary for arts category"
    state = run_agent(test_id='TestSummary:test2', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('category'), 'c_arts')
    
  def test3(self):
    request = "Summary for /rodeo channel?"
    state = run_agent(test_id='TestSummary:test3', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('channel'), 'rodeo-club')
    self.assertEqual(state.get('channel_url'), 'https://warpcast.com/~/channel/rodeo-club')
    
  def test4(self):
    request = "Summary of posts about the beauty of canadian landscapes"
    state = run_agent(test_id='TestSummary:test4', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertIsNotNone(state.get('search'))
      
  def test5(self):
    request = "Summary of @randombishop's posts"
    state = run_agent(test_id='TestSummary:test5', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user'), 'randombishop')
