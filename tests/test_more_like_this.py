from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestMoreLikeThis(unittest.TestCase):
  
  def assert_expected_output(self, state):
    self.assertEqual(state.action, 'MoreLikeThis')
    self.assertGreater(len(state.casts), 0)
    top_result = state.casts[0]
    SMALL_DISTANCE = 0.25
    self.assertLess(top_result['q_distance'], SMALL_DISTANCE)
    self.assertLess(top_result['dim_distance'], SMALL_DISTANCE)
  
  def test1(self):
    request = "More like this: Bitcoin is sweet!"
    state = run_bot(test_id='TestMoreLikeThis:1', request=request)
    self.assert_expected_output(state)
    
  def test2(self):
    parent_hash = '0x899f8e2fe0dd13241a336d7266273b1994476e86'
    request = "Find similar casts"
    state = run_bot(test_id='TestMoreLikeThis:2', request=request, parent_hash=parent_hash)
    self.assert_expected_output(state)

  def test3(self):
    attachment_hash = '0x677a180098d6a0dca3fc1c4002ffc2889eca7fc9'
    request = "Other casts like this one?"
    state = run_bot(test_id='TestMoreLikeThis:3', request=request, attachment_hash=attachment_hash)
    self.assert_expected_output(state)
    
  def test4(self):
    # test with a deleted parent
    parent_hash = '0xb59fcfda9e859be648e5d5541d292a6fb8cc9fcb'
    request = "More like this"
    run_bot(test_id='TestMoreLikeThis:4', request=request, parent_hash=parent_hash)
    