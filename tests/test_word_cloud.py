from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestWordCloud(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.get('intent'), 'WordCloud')
    self.assertIn('CreateWordCloud', state.get_tools_sequence())

  def test1(self):
    request = "Make @dwr.eth's word cloud."
    state = run_agent(test_id='TestWordCloud:1', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user_fid'), 3)
    self.assertEqual(state.get('user'), 'dwr.eth')
    
  def test2(self):
    request = "Make my word cloud."
    fid_origin = 253232
    state = run_agent(test_id='TestWordCloud:2', mode='bot', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user_fid'), fid_origin)
    self.assertEqual(state.get('user'), 'randombishop')
    
  def test3(self):
    request = "Make a word cloud for keyword 'bitcoin'"
    state = run_agent(test_id='TestWordCloud:3', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('keyword'), 'bitcoin')
    
  def test4(self):
    request = "Make a wordcloud for arts category"
    state = run_agent(test_id='TestWordCloud:4', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('category'), 'c_arts')
     
  def test5(self):
    request = "Make a wordcloud for /data channel?"
    state = run_agent(test_id='TestWordCloud:5', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('channel'), 'data')
    self.assertEqual(state.get('channel_url'), 'https://farcaster.group/data')

  def test6(self):
    request = "Make a word cloud about the beauty of canadian landscapes"
    state = run_agent(test_id='TestWordCloud:6', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertIsNotNone(state.get('search'))
      
  def test7(self):
    request = "Make a wordcloud for @randombishop's posts"
    state = run_agent(test_id='TestWordCloud:7', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user'), 'randombishop')
    
  def test8(self):
    request = "Make a word cloud for this channel"
    root_parent_url = "https://farcaster.group/data"
    state = run_agent(test_id='TestWordCloud:8', mode='bot', request=request, root_parent_url=root_parent_url)
    self.assert_expected_output(state)
    self.assertEqual(state.get('channel'), 'data')
    self.assertEqual(state.get('channel_url'), root_parent_url)
