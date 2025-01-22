import unittest
from bots.actions.digest_casts import DigestCasts
from bots.router import route


class TestDigestCasts(unittest.TestCase):
  
  def test1(self):
    request = "Give me a summary using keyword bitcoin"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, DigestCasts)
    self.assertEqual(action.keyword, 'bitcoin')
    self.assertIsNone(action.channel)
    self.assertIsNone(action.user_name)
    self.assertIsNone(action.search)
    self.assertGreaterEqual(len(action.casts), 3)
    
  def test2(self):
    request = "Summary for arts category"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, DigestCasts)
    self.assertEqual(action.category, 'c_arts')
    self.assertIsNone(action.channel)
    self.assertIsNone(action.keyword)
    self.assertIsNone(action.user_name)
    self.assertIsNone(action.search)
    self.assertGreaterEqual(len(action.casts), 3)
    
  def test3(self):
    request = "Summary for /data channel?"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, DigestCasts)
    self.assertEqual(action.channel, 'https://farcaster.group/data')
    self.assertIsNone(action.keyword)
    self.assertIsNone(action.category)
    self.assertIsNone(action.user_name)
    self.assertIsNone(action.search)
    self.assertGreaterEqual(len(action.casts), 3)

  def test4(self):
    request = "Summary of posts about the beauty of canadian landscapes"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, DigestCasts)
    self.assertIsNotNone(action.search)
    self.assertGreaterEqual(len(action.casts), 3)
      
  def test5(self):
    request = "Summary of @randombishop's posts"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, DigestCasts)
    self.assertEqual(action.user_name, 'randombishop')
    self.assertIsNone(action.keyword)
    self.assertIsNone(action.category)
    self.assertIsNone(action.channel)
    self.assertIsNone(action.search)
    self.assertGreaterEqual(len(action.casts), 3)
