from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestMoreLikeThis(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.get('intent'), 'MoreLikeThis')
    self.assertIn('ParseMoreLikeThisText', state.get_tools_sequence())
    self.assertIn('GetMoreLikeThis', state.get_tools_sequence())
    casts = state.get('data_casts_text')
    self.assertGreater(len(casts), 0)
    top_result = casts[0]
    SMALL_DISTANCE = 0.25
    self.assertLess(top_result['q_distance'], SMALL_DISTANCE)
    self.assertLess(top_result['dim_distance'], SMALL_DISTANCE)
  
  def test1(self):
    request = "More like this: Bitcoin is sweet!"
    state = run_agent(test_id='TestMoreLikeThis:1', mode='bot', request=request)
    self.assert_expected_output(state)
    
  def test2(self):
    parent_hash = '0x899f8e2fe0dd13241a336d7266273b1994476e86'
    request = "Find similar casts"
    state = run_agent(test_id='TestMoreLikeThis:2', mode='bot', request=request, parent_hash=parent_hash)
    self.assert_expected_output(state)

  def test3(self):
    attachment_hash = '0x677a180098d6a0dca3fc1c4002ffc2889eca7fc9'
    request = "Other casts like this one?"
    state = run_agent(test_id='TestMoreLikeThis:3', mode='bot', request=request, attachment_hash=attachment_hash)
    self.assert_expected_output(state)
    
  
    