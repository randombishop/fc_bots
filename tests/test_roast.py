import unittest
from bots.actions.roast import Roast
from bots.router import route


class TestRoast(unittest.TestCase):
  
  def test1(self):
    request = "Roast randombishop"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, Roast)
    self.assertEqual(action.fid, 253232)
    self.assertEqual(action.user_name, 'randombishop')
    self.assertEqual(len(action.casts), 1)
    
  def test2(self):
    request = "roast me"
    fid_origin = 253232
    action = route(request, fid_origin=fid_origin)
    action.run()
    action.print()
    self.assertIsInstance(action, Roast)
    self.assertEqual(action.fid, fid_origin)
    self.assertEqual(action.user_name, 'randombishop')
    self.assertEqual(len(action.casts), 1)