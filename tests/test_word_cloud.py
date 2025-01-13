import unittest
from bots.actions.word_cloud import WordCloud
from bots.router import route


class TestWordCloud(unittest.TestCase):
  
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
    fid_origin = 253232
    action = route(request, fid_origin=fid_origin)
    action.run()
    action.print()
    self.assertIsInstance(action, WordCloud)
    self.assertEqual(action.fid, fid_origin)
    self.assertEqual(action.user_name, 'randombishop')
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
    
  def test3(self):
    request = "Make a word cloud for keyword 'bitcoin'"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, WordCloud)
    self.assertEqual(action.keyword, 'bitcoin')
    self.assertIsNone(action.channel)
    self.assertIsNone(action.user_name)
    self.assertIsNone(action.search)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
    
  def test4(self):
    request = "Make a wordcloud for arts category"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, WordCloud)
    self.assertEqual(action.category, 'c_arts')
    self.assertIsNone(action.channel)
    self.assertIsNone(action.keyword)
    self.assertIsNone(action.user_name)
    self.assertIsNone(action.search)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
    
  def test5(self):
    request = "Make a wordcloud for /data channel?"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, WordCloud)
    self.assertEqual(action.channel, 'https://farcaster.group/data')
    self.assertIsNone(action.keyword)
    self.assertIsNone(action.category)
    self.assertIsNone(action.user_name)
    self.assertIsNone(action.search)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)

  def test6(self):
    request = "Make a word cloud about the beauty of canadian landscapes"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, WordCloud)
    self.assertIsNotNone(action.search)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
      
  def test7(self):
    request = "Make a wordcloud for @randombishop's posts"
    action = route(request)
    action.run()
    action.print()
    self.assertIsInstance(action, WordCloud)
    self.assertEqual(action.user_name, 'randombishop')
    self.assertIsNone(action.keyword)
    self.assertIsNone(action.category)
    self.assertIsNone(action.channel)
    self.assertIsNone(action.search)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
    
  def test8(self):
    request = "Make a word cloud for this channel"
    root_parent_url = "https://farcaster.group/data"
    action = route(request, root_parent_url=root_parent_url)
    action.run()
    action.print()
    self.assertIsInstance(action, WordCloud)
    self.assertEqual(action.channel, root_parent_url)
    self.assertIsNone(action.user_name)
    self.assertEqual(len(action.casts), 1)
    self.assertEqual(len(action.casts[0]['embeds']), 1)
