from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent



class TestConversation(unittest.TestCase):
  
  def test1(self):
    state = run_agent(test_id='TestConversation:1', mode='blueprint', blueprint=[])
    self.assertIsNotNone(state.get_variable('bio'))
    self.assertIsNotNone(state.get_variable('lore'))
    self.assertIsNotNone(state.get_variable('style'))
    self.assertIsNotNone(state.get_variable('time'))
    self.assertIsNone(state.get_variable('conversation'))
    
  def test2(self):
    request = 'Hello World'
    state = run_agent(test_id='TestConversation:2', request=request, mode='blueprint', blueprint=[])
    conversation = str(state.get_variable('conversation'))
    self.assertIn(request, conversation)
    self.assertEqual(state.request, request)  

  def test3(self):
    request = "Find similar casts"
    parent_hash = '0x8fa5e35f8b843c1713a2c4d32a59edc6a2abb863'
    state = run_agent(test_id='TestConversation:2', request=request, parent_hash=parent_hash, mode='blueprint', blueprint=[])
    conversation = str(state.get_variable('conversation'))
    self.assertIn(request, conversation)
    self.assertIn('@v', conversation)
    self.assertIn('@unknown_user', conversation)
    
  def test4(self):
    request = "Other casts like this one?"
    attachment_hash = '0xbe89c48299d8b080267ddd96c06c84397ee13185'
    state = run_agent(test_id='TestConversation:4', request=request, attachment_hash=attachment_hash, mode='blueprint', blueprint=[])
    conversation = str(state.get_variable('conversation'))
    self.assertIn(request, conversation)  
    self.assertIn('@unknown_user', conversation)
    self.assertIn('quoting @ds007', conversation)
    self.assertIn('I like #DataScience and #ML therefore I like #Farcaster', conversation)
    
  def test5(self):
    request = "More like this"
    fid_origin = 253232
    parent_hash = '0x6f119aad7fa236cd31eeebd03d569bc264350d29'
    state = run_agent(test_id='TestConversation:5', request=request, fid_origin=fid_origin, parent_hash=parent_hash, mode='blueprint', blueprint=[])
    conversation = str(state.get_variable('conversation'))
    user_origin = state.get_variable('user_origin')
    self.assertIn(request, conversation)
    self.assertIn('@horsefacts.eth', conversation)
    self.assertIn('@randombishop', conversation)
    self.assertIn('post a picture of you from a different era', conversation)
    self.assertEqual(user_origin.fid, 253232)
    self.assertEqual(user_origin.username, 'randombishop')

  def test6(self):
    request = "Deleted parent test"
    parent_hash = '0xb59fcfda9e859be648e5d5541d292a6fb8cc9fcb'
    state = run_agent(test_id='TestConversation:5', request=request, parent_hash=parent_hash, mode='blueprint', blueprint=[])
    conversation = str(state.get_variable('conversation'))
    self.assertIn(request, conversation)
    
  
