import unittest
from bots.actions.most_active_users import MostActiveUsers
from bots.router import route


class TestMostActiveUsers(unittest.TestCase):
  
  def test1(self):
    request = "Who is most active in channel /politics?"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, MostActiveUsers)
    self.assertEqual(action.channel, 'https://warpcast.com/~/channel/politics')
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['mentions']), 3)
