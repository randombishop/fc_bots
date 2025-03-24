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
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['fid'], 5650)
    self.assertEqual(state.action_params['user_name'], 'vitalik.eth')
    
  def test2(self):
    request = "Make my word cloud."
    fid_origin = 253232
    state = run_bot(request, fid_origin=fid_origin)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['fid'], fid_origin)
    self.assertEqual(state.action_params['user_name'], 'randombishop')
    
  def test3(self):
    request = "Make a word cloud for keyword 'bitcoin'"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['keyword'], 'bitcoin')
    
  def test4(self):
    request = "Make a wordcloud for arts category"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['category'], 'c_arts')
     
  def test5(self):
    request = "Make a wordcloud for /data channel?"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['channel'], 'https://farcaster.group/data')

  def test6(self):
    request = "Make a word cloud about the beauty of canadian landscapes"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertIsNotNone(state.action_params['search'])
      
  def test7(self):
    request = "Make a wordcloud for @randombishop's posts"
    state = run_bot(request)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['user_name'], 'randombishop')
    
  def test8(self):
    request = "Make a word cloud for this channel"
    root_parent_url = "https://farcaster.group/data"
    state = run_bot(request, root_parent_url=root_parent_url)
    self.assert_expected_output(state)
    self.assertEqual(state.action_params['channel'], root_parent_url)
