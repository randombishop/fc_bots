import unittest
from bots.actions.more_like_this import MoreLikeThis
from bots.router import route


class TestMoreLikeThis(unittest.TestCase):

  def test1(self):
    request = "More like this: #Bitcoin is sweet!"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, MoreLikeThis)
    self.assertGreater(len(action.casts), 0)
    top_result = action.data[0]
    self.assertLess(top_result['q_distance'], 0.1)
    self.assertLess(top_result['dim_distance'], 0.1)

  def test2(self):
    parent_hash = '0x8fa5e35f8b843c1713a2c4d32a59edc6a2abb863'
    request = "Find similar casts"
    action = route(request)
    action.set_parent_hash(parent_hash)
    action.run()
    action.print()
    self.assertIsInstance(action, MoreLikeThis)
    self.assertGreater(len(action.casts), 0)
    hashes = [cast['embeds'][0]['hash'] for cast in action.casts]
    self.assertNotIn(parent_hash, hashes)

  def test3(self):
    attachment_hash = '0xbe89c48299d8b080267ddd96c06c84397ee13185'
    request = "Other casts like this one?"
    action = route(request)
    action.set_attachment_hash(attachment_hash)
    action.run()
    action.print()
    self.assertIsInstance(action, MoreLikeThis)
    self.assertGreater(len(action.casts), 0)
    hashes = [cast['embeds'][0]['hash'] for cast in action.casts]
    self.assertNotIn(attachment_hash, hashes)