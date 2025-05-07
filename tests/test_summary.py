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
    keywords = state.get_variable_values('Keyword')
    self.assertIn('ethereum', [x.keyword for x in keywords])
      
  def test2(self):
    request = "Summary for /rodeo channel?"
    state = run_agent(test_id='TestSummary:test2', mode='bot', request=request)
    self.assert_expected_output(state)
    channels = state.get_variable_values('ChannelId')
    self.assertEqual(len(channels), 1)
    self.assertEqual(channels[0].channel, 'rodeo-club')
    self.assertEqual(channels[0].channel_url, 'https://warpcast.com/~/channel/rodeo-club')
    
  def test3(self):
    request = "Summary of posts about the beauty of Canada"
    state = run_agent(test_id='TestSummary:test3', mode='bot', request=request)
    search_phrases = state.get_variable_values('SearchPhrase')
    self.assert_expected_output(state)
    self.assertIn('canada', search_phrases[0].search.lower())
      
  def test4(self):
    request = "Summary of @randombishop's posts"
    state = run_agent(test_id='TestSummary:test4', mode='bot', request=request)
    self.assert_expected_output(state)
    users = state.get_variable_values('UserId')
    self.assertEqual(users[0].username, 'randombishop')
    self.assertEqual(users[0].fid, 253232)
