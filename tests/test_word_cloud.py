from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestWordCloud(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.plan['intent'], 'WordCloud')
    images = state.get_variable_values('WordCloudImage')
    self.assertEqual(len(images), 1)
    self.assertTrue(state.valid)

  def test1(self):
    request = "Make @dwr.eth's word cloud."
    state = run_agent(test_id='TestWordCloud:1', mode='bot', request=request)
    self.assert_expected_output(state)
    user = state.get_variable_values('UserId')[-1]
    self.assertEqual(user.fid, 3)
    self.assertEqual(user.username, 'dwr.eth')
    
  def test2(self):
    request = "Make my word cloud."
    fid_origin = 253232
    state = run_agent(test_id='TestWordCloud:2', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    user = state.get_variable_values('UserId')[-1]
    self.assertEqual(user.fid, fid_origin)
    self.assertEqual(user.username, 'randombishop')
    
  def test3(self):
    request = "Make a word cloud for keyword 'bitcoin'"
    state = run_agent(test_id='TestWordCloud:3', mode='bot', request=request)
    self.assert_expected_output(state)
    keywords = state.get_variable_values('Keyword')
    self.assertEqual(len(keywords), 1)
    self.assertEqual(keywords[0].keyword, 'bitcoin')
    
  def test4(self):
    request = "Make a wordcloud for /data channel?"
    state = run_agent(test_id='TestWordCloud:4', mode='bot', request=request)
    self.assert_expected_output(state)
    channels = state.get_variable_values('ChannelId')
    self.assertEqual(len(channels), 1)
    self.assertEqual(channels[0].channel, 'data')
    self.assertEqual(channels[0].channel_url, 'https://farcaster.group/data')

  def test5(self):
    request = "Make a word cloud about the beauty of canada"
    state = run_agent(test_id='TestWordCloud:5', mode='bot', request=request)
    self.assert_expected_output(state)
    search_phrases = state.get_variable_values('SearchPhrase')
    self.assertEqual(len(search_phrases), 1)
    self.assertIn('canada', search_phrases[0].search.lower())
    
  def test6(self):
    request = "Make a wordcloud for @randombishop's posts"
    state = run_agent(test_id='TestWordCloud:6', mode='bot', request=request)
    self.assert_expected_output(state)            
    user = state.get_variable_values('UserId')[-1]
    self.assertEqual(user.fid, 253232)
    self.assertEqual(user.username, 'randombishop')  
      
  def test7(self):
    request = "Make a word cloud for this channel"
    root_parent_url = "https://farcaster.group/data"
    state = run_agent(test_id='TestWordCloud:7', mode='bot', request=request, root_parent_url=root_parent_url)
    self.assert_expected_output(state)
    channels = state.get_variable_values('ChannelId')
    self.assertEqual(channels[-1].channel, 'data')
    self.assertEqual(channels[-1].channel_url, root_parent_url)
