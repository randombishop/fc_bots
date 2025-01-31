import unittest
from bots.action.news import News
from bots.router import route


class TestNews(unittest.TestCase):
  
  def test1(self):
    request = "Search the news for Data Science"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, News)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
