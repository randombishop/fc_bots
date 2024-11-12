import unittest
from bots.actions.chat import Chat
from bots.router import route


class TestChat(unittest.TestCase):
  
  def test1(self):
    request = "whats the point?"
    fid_origin=644823
    parent_hash='0xbb517c8bd0694028bc926178bdddbf87e281b6b8'
    action = route(request, fid_origin, parent_hash)
    action.run()
    action.print()
    self.assertIsInstance(action, Chat)
    self.assertEqual(len(action.casts), 1)
    