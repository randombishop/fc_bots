from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestPickCast(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'Pick')
    self.assertEqual(len(state.casts), 1)
    self.assertEqual(len(state.casts[0]['embeds']), 1)
    
  def test1(self):
    request = "Pick the most beautiful cast in arts category"
    state = run_bot(test_id='TestPickCast:1', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.category, 'c_arts')
    self.assertIn('beautiful', state.criteria)
            
  def test2(self):
    request = "Pick the funniest cast from /parenting channel"
    state = run_bot(test_id='TestPickCast:2', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.channel, 'parenting')
    self.assertEqual(state.channel_url, 'chain://eip155:8453/erc721:0xb7310fc4b4a31c4fb7adf90b8201546bb2bcb52c')
    self.assertIn('fun', state.criteria)

  def test3(self):
    request = "Pick the most intriguing cast from @randombishop"
    state = run_bot(test_id='TestPickCast:3', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.user, 'randombishop')
    self.assertIn('intrig', state.criteria)
    
  def test4(self):
    request = "Pick the funniest cast in channnel /data?"
    state = run_bot(test_id='TestPickCast:4', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.channel, 'data')
    self.assertEqual(state.channel_url, 'https://farcaster.group/data')
    self.assertIn('fun', state.criteria)