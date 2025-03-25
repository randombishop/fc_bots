from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestWordCloud(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'WordCloud')
    self.assertEqual(len(state.casts), 1)
    self.assertEqual(len(state.casts[0]['embeds']), 1)

  def test1(self):
    request = "Make @vitalik.eth's word cloud."
    state = run_bot(test_id='TestWordCloud:1', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.user_fid, 5650)
    self.assertEqual(state.user, 'vitalik.eth')
    
  def test2(self):
    request = "Make my word cloud."
    fid_origin = 253232
    state = run_bot(test_id='TestWordCloud:2', request=request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.user_fid, fid_origin)
    self.assertEqual(state.user, 'randombishop')
    
  def test3(self):
    request = "Make a word cloud for keyword 'bitcoin'"
    state = run_bot(test_id='TestWordCloud:3', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.keyword, 'bitcoin')
    
  def test4(self):
    request = "Make a wordcloud for arts category"
    state = run_bot(test_id='TestWordCloud:4', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.category, 'c_arts')
     
  def test5(self):
    request = "Make a wordcloud for /data channel?"
    state = run_bot(test_id='TestWordCloud:5', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.channel, 'data')
    self.assertEqual(state.channel_url, 'https://farcaster.group/data')

  def test6(self):
    request = "Make a word cloud about the beauty of canadian landscapes"
    state = run_bot(test_id='TestWordCloud:6', request=request)
    self.assert_expected_output(state)
    self.assertIsNotNone(state.search)
      
  def test7(self):
    request = "Make a wordcloud for @randombishop's posts"
    state = run_bot(test_id='TestWordCloud:7', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.user, 'randombishop')
    
  def test8(self):
    request = "Make a word cloud for this channel"
    root_parent_url = "https://farcaster.group/data"
    state = run_bot(test_id='TestWordCloud:8', request=request, root_parent_url=root_parent_url)
    self.assert_expected_output(state)
    self.assertEqual(state.channel, 'data')
    self.assertEqual(state.channel_url, root_parent_url)
