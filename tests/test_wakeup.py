from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_tool_input
from bots.tools.wakeup.get_bio import GetBio
from bots.tools.wakeup.get_lore import GetLore
from bots.tools.wakeup.get_style import GetStyle
from bots.tools.wakeup.get_time import GetTime
from bots.tools.wakeup.get_conversation import GetConversation


class TestWakeUp(unittest.TestCase):
  
  def test_bio(self):
    input = make_tool_input()
    GetBio.invoke({'input': input})
    self.assertIsNotNone(input.state.bio)
    
  def test_lore(self):
    input = make_tool_input()
    GetLore.invoke({'input': input})
    self.assertIsNotNone(input.state.lore)
    
  def test_style(self):
    input = make_tool_input()
    GetStyle.invoke({'input': input})
    self.assertIsNotNone(input.state.style)
    
  def test_time(self):
    input = make_tool_input()
    GetTime.invoke({'input': input})
    self.assertIsNotNone(input.state.time)
    
  

  #########################################################
  # Conversation examples
  #########################################################
  
  def test_conversation1(self):
    input = make_tool_input()
    input.state.request = "Hello World"
    GetConversation.invoke({'input': input})
    self.assertIn(input.state.request, input.state.conversation)

  def test_conversation2(self):
    input = make_tool_input()
    input.state.request = "Find similar casts"
    input.state.parent_hash = '0x8fa5e35f8b843c1713a2c4d32a59edc6a2abb863'
    GetConversation.invoke({'input': input})
    self.assertIn(input.state.request, input.state.conversation)
    self.assertIn('@v', input.state.conversation)
    self.assertIn('@unknown_user', input.state.conversation)
    
  def test_conversation3(self):
    input = make_tool_input()
    input.state.request = "Other casts like this one?"
    input.state.attachment_hash = '0xbe89c48299d8b080267ddd96c06c84397ee13185'
    GetConversation.invoke({'input': input})
    self.assertIn(input.state.request, input.state.conversation)
    self.assertIn('@unknown_user', input.state.conversation)
    self.assertIn('quoting @ds007', input.state.conversation)
    self.assertIn('I like #DataScience and #ML therefore I like #Farcaster', input.state.conversation)
    
  def test_conversation4(self):
    input = make_tool_input()
    input.state.request = "More like this"
    input.state.fid_origin = 253232
    input.state.parent_hash = '0x6f119aad7fa236cd31eeebd03d569bc264350d29'
    GetConversation.invoke({'input': input})
    self.assertIn(input.state.request, input.state.conversation)
    self.assertIn('@horsefacts.eth', input.state.conversation)
    self.assertIn('@randombishop', input.state.conversation)
    self.assertIn('quoting @greg', input.state.conversation)
    self.assertIn('post a picture of you from a different era', input.state.conversation)

  def test_conversation5(self):
    input = make_tool_input()
    input.state.request = "Deleted parent test"
    input.state.parent_hash = '0xb59fcfda9e859be648e5d5541d292a6fb8cc9fcb'
    GetConversation.invoke({'input': input})
    self.assertIn(input.state.request, input.state.conversation)
    
