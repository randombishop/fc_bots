import unittest
from bots.actions.word_cloud import WordCloud
from bots.router import route


class TestFavoriteUsers(unittest.TestCase):
  
  def test1(self):
    request = "Make @vitalik.eth's word cloud."
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, WordCloud)
    self.assertEqual(action.fid, 5650)
    self.assertEqual(action.user_name, 'vitalik.eth')
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
    
  def test2(self):
    request = "Make my word cloud."
    fid_origin = 5650
    action = route(request, fid_origin=fid_origin)
    action.run()
    action.print()
    self.assertIsInstance(action, WordCloud)
    self.assertEqual(action.fid, fid_origin)
    self.assertEqual(action.user_name, 'vitalik.eth')
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)