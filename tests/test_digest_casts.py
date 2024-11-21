import unittest
from bots.actions.digest_casts import DigestCasts
from bots.router import route


class TestDigestCasts(unittest.TestCase):
  
  def test1(self):
    request = "Give me a daily digest about bitcoin"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, DigestCasts)
    self.assertIsNone(action.channel)
    self.assertEqual(action.keyword, 'bitcoin')
    self.assertEqual(action.category, 'c_crypto')
    self.assertGreaterEqual(len(action.casts), 3)
    
  def test2(self):
    request = "Summary for arts category"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, DigestCasts)
    self.assertIsNone(action.channel)
    self.assertIsNone(action.keyword)
    self.assertEqual(action.category, 'c_arts')
    self.assertGreaterEqual(len(action.casts), 3)
    
  def test3(self):
    request = "Digest /data channel?"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, DigestCasts)
    self.assertEqual(action.channel, 'https://farcaster.group/data')
    self.assertIsNone(action.keyword)
    self.assertIsNone(action.category)
    self.assertGreaterEqual(len(action.casts), 3)