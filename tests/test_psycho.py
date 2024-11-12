import unittest
from bots.actions.psycho import Psycho
from bots.router import route


class TestPsycho(unittest.TestCase):
  
  def test1(self):
    request = "Psycho analyze @randombishop"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, Psycho)
    self.assertEqual(action.fid, 253232)
    self.assertEqual(action.user, 'randombishop')
    self.assertEqual(len(action.casts), 3)
    
  def test2(self):
    request = "psycho analyze me"
    fid_origin = 253232
    action = route(request, fid_origin=fid_origin)
    action.run()
    action.print()
    self.assertIsInstance(action, Psycho)
    self.assertEqual(action.fid, fid_origin)
    self.assertEqual(action.user, 'randombishop')
    self.assertEqual(len(action.casts), 3)