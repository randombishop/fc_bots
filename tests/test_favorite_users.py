import unittest
from bots.action.favorite_users import FavoriteUsers
from bots.router import route


class TestFavoriteUsers(unittest.TestCase):
  
  def test1(self):
    request = "Who are @dwr.eth's favorite users?"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, FavoriteUsers)
    self.assertEqual(action.fid, 3)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['mentions']), 3)
    
  def test2(self):
    request = "Who are my favorite users?"
    fid_origin = 2
    action = route(request, fid_origin=fid_origin)
    action.run()
    action.print()
    self.assertIsInstance(action, FavoriteUsers)
    self.assertEqual(action.fid, fid_origin)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['mentions']), 3)
    
  def test3(self):
    request = "Who are this guy's favorite users?"
    fid_origin = 874939
    parent_hash = '0x86e946e7ffe837e0a27ae70f60826337028394d7'
    fid_target = 253232
    action = route(request, fid_origin=fid_origin, parent_hash=parent_hash)
    action.run()
    action.print()
    self.assertIsInstance(action, FavoriteUsers)
    self.assertEqual(action.fid, fid_target)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['mentions']), 3)
