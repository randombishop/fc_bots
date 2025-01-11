import unittest
from bots.actions.like import Like
from bots.router import route


class TestLike(unittest.TestCase):
  
  def test1(self):
    request = "Thank you!"
    fid_origin=253232
    action = route(request, fid_origin)
    action.run()
    action.print()
    self.assertIsInstance(action, Like)
    self.assertTrue(action.casts[0]['like'])
    
  def test2(self):
    request = "Not interested."
    fid_origin=253232
    action = route(request, fid_origin)
    action.run()
    action.print()
    self.assertIsInstance(action, Like)
    self.assertEqual(len(action.casts), 0)
    