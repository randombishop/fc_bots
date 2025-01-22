import unittest
from bots.actions.more_like_this import MoreLikeThis
from bots.router import get_context


class TestGetContext(unittest.TestCase):

  def test1(self):
    request = "Hello World"
    context = get_context(request)
    self.assertEqual(len(context), 1)
    self.assertEqual(context[0]['text'], request)
    self.assertEqual(context[0]['fid'], None)
    self.assertEqual(context[0]['username'], 'unknown_user')

  def test2(self):
    request = "Find similar casts"
    parent_hash = '0x8fa5e35f8b843c1713a2c4d32a59edc6a2abb863'
    context = get_context(request, parent_hash=parent_hash)
    self.assertEqual(len(context), 2)
    self.assertEqual(context[0]['fid'], 2)
    self.assertEqual(context[0]['username'], 'v')
    self.assertEqual(context[1]['text'], request)
    self.assertEqual(context[1]['username'], 'unknown_user')
    
  def test3(self):
    attachment_hash = '0xbe89c48299d8b080267ddd96c06c84397ee13185'
    request = "Other casts like this one?"
    context = get_context(request, attachment_hash=attachment_hash)
    self.assertEqual(len(context), 1)
    self.assertEqual(context[0]['text'], request)
    self.assertEqual(context[0]['fid'], None)
    self.assertEqual(context[0]['username'], 'unknown_user')
    self.assertEqual(context[0]['quote']['fid'], 874939)
    self.assertEqual(context[0]['quote']['username'], 'ds007')
    self.assertEqual(context[0]['quote']['text'], 'I like #DataScience and #ML therefore I like #Farcaster')
    
  def test4(self):
    request = "More like this"
    fid_origin = 253232
    parent_hash = '0x6f119aad7fa236cd31eeebd03d569bc264350d29'
    context = get_context(request, fid_origin=fid_origin, parent_hash=parent_hash)
    self.assertEqual(len(context), 2)
    self.assertEqual(context[0]['fid'], 3621)
    self.assertEqual(context[0]['username'], 'horsefacts.eth')
    self.assertEqual(context[0]['quote']['fid'], 347)
    self.assertEqual(context[0]['quote']['username'], 'greg')
    self.assertEqual(context[0]['quote']['text'], 'post a picture of you from a different era')
    self.assertEqual(context[1]['text'], request)
    self.assertEqual(context[1]['fid'], 253232)
    self.assertEqual(context[1]['username'], 'randombishop')
