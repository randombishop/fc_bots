from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_tool_input
from bots.tools.init.get_bio import GetBio
from bots.tools.init.get_lore import GetLore
from bots.tools.init.get_style import GetStyle
from bots.tools.init.get_time import GetTime
from bots.tools.init.get_conversation import GetConversation


class TestWakeUp(unittest.TestCase):
  
  def test_bio(self):
    input = make_tool_input()
    result = GetBio.invoke({'input': input})
    self.assertIsNotNone(result['bio'])
    
  def test_lore(self):
    input = make_tool_input()
    result = GetLore.invoke({'input': input})
    self.assertIsNotNone(result['lore'])
    
  def test_style(self):
    input = make_tool_input()
    result = GetStyle.invoke({'input': input})
    self.assertIsNotNone(result['style'])
    
  def test_time(self):
    input = make_tool_input()
    result = GetTime.invoke({'input': input})
    self.assertIsNotNone(result['time'])
    
  

  #########################################################
  # Conversation examples
  #########################################################
  
  def test_conversation1(self):
    request = 'Hello World'
    input = make_tool_input({'request': request})
    result = GetConversation.invoke({'input': input})
    self.assertIn(request, result['conversation'])  

  def test_conversation2(self):
    request = "Find similar casts"
    parent_hash = '0x8fa5e35f8b843c1713a2c4d32a59edc6a2abb863'
    input = make_tool_input({'request': request, 'parent_hash': parent_hash})
    result = GetConversation.invoke({'input': input})
    self.assertIn(request, result['conversation'])
    self.assertIn('@v', result['conversation'])
    self.assertIn('@unknown_user', result['conversation'])
    
  def test_conversation3(self):
    request = "Other casts like this one?"
    attachment_hash = '0xbe89c48299d8b080267ddd96c06c84397ee13185'
    input = make_tool_input({'request': request, 'attachment_hash': attachment_hash})
    result = GetConversation.invoke({'input': input})
    self.assertIn(request, result['conversation'])  
    self.assertIn('@unknown_user', result['conversation'])
    self.assertIn('quoting @ds007', result['conversation'])
    self.assertIn('I like #DataScience and #ML therefore I like #Farcaster', result['conversation'])
    
  def test_conversation4(self):
    request = "More like this"
    fid_origin = 253232
    parent_hash = '0x6f119aad7fa236cd31eeebd03d569bc264350d29'
    input = make_tool_input({'request': request, 'fid_origin': fid_origin, 'parent_hash': parent_hash})
    result = GetConversation.invoke({'input': input})
    self.assertIn(request, result['conversation'])
    self.assertIn('@horsefacts.eth', result['conversation'])
    self.assertIn('@randombishop', result['conversation'])
    self.assertIn('quoting @greg', result['conversation'])
    self.assertIn('post a picture of you from a different era', result['conversation'])

  def test_conversation5(self):
    request = "Deleted parent test"
    parent_hash = '0xb59fcfda9e859be648e5d5541d292a6fb8cc9fcb'
    input = make_tool_input({'request': request, 'parent_hash': parent_hash})
    result = GetConversation.invoke({'input': input})
    self.assertIn(request, result['conversation'])
    
  def test_conversation6(self):
    parent_hash = '0xb59fcfda9e859be648e5d5541d292a6fb8cc9fcb'
    request = "Parent is deleted but this should not fail"
    input = make_tool_input({'request': request, 'parent_hash': parent_hash})
    result = GetConversation.invoke({'input': input})
    self.assertIn(request, result['conversation'])
    
