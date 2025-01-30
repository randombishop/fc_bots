import unittest
from bots.actions.more_like_this import MoreLikeThis
from bots.router import route


SMALL_DISTANCE = 0.25

class TestMoreLikeThis(unittest.TestCase):

  def test1(self):
    request = "More like this: Bitcoin is sweet!"
    action = route(request)
    action.run()
    action.print()
    top_result = action.data[0]
    self.assertIsInstance(action, MoreLikeThis)
    self.assertGreater(len(action.casts), 0)
    self.assertLess(top_result['q_distance'], SMALL_DISTANCE)
    self.assertLess(top_result['dim_distance'], SMALL_DISTANCE)

  def test2(self):
    parent_hash = '0x899f8e2fe0dd13241a336d7266273b1994476e86'
    request = "Find similar casts"
    action = route(request, parent_hash=parent_hash)
    action.run()
    action.print()
    hashes = [cast['embeds'][0]['hash'] for cast in action.casts]
    top_result = action.data[0]
    self.assertIsInstance(action, MoreLikeThis)
    self.assertGreater(len(action.casts), 0)
    #self.assertNotIn(parent_hash, hashes)
    self.assertLess(top_result['q_distance'], SMALL_DISTANCE)
    self.assertLess(top_result['dim_distance'], SMALL_DISTANCE)

  def test3(self):
    attachment_hash = '0x677a180098d6a0dca3fc1c4002ffc2889eca7fc9'
    request = "Other casts like this one?"
    action = route(request, attachment_hash=attachment_hash)
    action.run()
    action.print()
    hashes = [cast['embeds'][0]['hash'] for cast in action.casts]
    top_result = action.data[0]
    self.assertIsInstance(action, MoreLikeThis)
    self.assertGreater(len(action.casts), 0)
    #self.assertNotIn(attachment_hash, hashes)
    self.assertLess(top_result['q_distance'], SMALL_DISTANCE)
    self.assertLess(top_result['dim_distance'], SMALL_DISTANCE)
    
  def test4(self):
    # test with a deleted parent
    parent_hash = '0xb59fcfda9e859be648e5d5541d292a6fb8cc9fcb'
    request = "More like this"
    action = route(request, parent_hash=parent_hash)
    action.run()
    action.print()
    