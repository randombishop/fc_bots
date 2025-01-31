import unittest
from bots.action.pick_cast import PickCast
from bots.router import route


class TestPickCast(unittest.TestCase):
    
  def test1(self):
    request = "Pick the most beautiful cast in arts category"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, PickCast)
    self.assertEqual(action.category, 'c_arts')
    self.assertIn('beautiful', action.criteria)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
    
  def test2(self):
    request = "Pick the funniest cast from /parenting channel"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, PickCast)
    self.assertEqual(action.channel, 'chain://eip155:8453/erc721:0xb7310fc4b4a31c4fb7adf90b8201546bb2bcb52c')
    self.assertIn('fun', action.criteria)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
    
  def test3(self):
    request = "Pick the most intriguing cast from @randombishop"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, PickCast)
    self.assertEqual(action.user_name, 'randombishop')
    self.assertIn('intrig', action.criteria)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)