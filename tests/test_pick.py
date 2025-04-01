from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestPickCast(unittest.TestCase):

  def assert_expected_output(self, state):
    self.assertIsNotNone(state.get('data_casts')[0]['embeds'])
    
  def test1(self):
    request = "Pick the most beautiful cast in arts category"
    state = run_agent(test_id='TestPickCast:1', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('category'), 'c_arts')
            
  def test2(self):
    request = "Pick the funniest cast from /parenting channel"
    state = run_agent(test_id='TestPickCast:2', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('channel'), 'parenting')
    self.assertEqual(state.get('channel_url'), 'chain://eip155:8453/erc721:0xb7310fc4b4a31c4fb7adf90b8201546bb2bcb52c')

  def test3(self):
    request = "Pick the most intriguing cast from @randombishop"
    state = run_agent(test_id='TestPickCast:3', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('user'), 'randombishop')
    
  def test4(self):
    request = "Pick the funniest cast in channnel /data?"
    state = run_agent(test_id='TestPickCast:4', mode='bot', request=request)
    self.assert_expected_output(state)
    self.assertEqual(state.get('channel'), 'data')
    self.assertEqual(state.get('channel_url'), 'https://farcaster.group/data')
