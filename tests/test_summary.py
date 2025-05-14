from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestSummary(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.get_selected_intent(), 'Summary')
    self.assertTrue(state.is_valid())
      
  def test1(self):
    request = "Give me a summary using keyword ethereum"
    state = run_agent(test_id='TestSummary:test1', mode='bot', request=request)
    self.assert_expected_output(state)
    keywords = state.get_variable_values_by_type('Keyword')
    self.assertIn('ethereum', [x.keyword for x in keywords])
      
  def test2(self):
    request = "Summary for /rodeo channel?"
    state = run_agent(test_id='TestSummary:test2', mode='bot', request=request)
    self.assert_expected_output(state)
    channel = state.get_last_variable_value_by_type('ChannelId')
    self.assertEqual(channel.channel, 'rodeo-club')
    self.assertEqual(channel.channel_url, 'https://warpcast.com/~/channel/rodeo-club')
    
  def test3(self):
    request = "Summary of posts about the beauty of canada"
    state = run_agent(test_id='TestSummary:test3', mode='bot', request=request)
    search_phrase = state.get_last_variable_value_by_type('SearchPhrase')
    self.assert_expected_output(state)
    self.assertIn('canada', search_phrase.search.lower())
      
  def test4(self):
    request = "Summary of @randombishop's posts"
    state = run_agent(test_id='TestSummary:test4', mode='bot', request=request)
    self.assert_expected_output(state)
    user = state.get_last_variable_value_by_type('UserId')
    self.assertEqual(user.username, 'randombishop')
    self.assertEqual(user.fid, 253232)
