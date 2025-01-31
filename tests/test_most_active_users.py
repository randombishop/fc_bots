import unittest
from bots.action.most_active_users import MostActiveUsers
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
    
  def test2(self):
    request = "Who is most active here?"
    channel_url = 'https://farcaster.group/data'
    action = route(request, root_parent_url=channel_url)
    action.run()
    action.print()
    self.assertIsInstance(action, MostActiveUsers)
    self.assertEqual(action.channel, channel_url)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['mentions']), 3)
