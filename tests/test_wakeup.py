import unittest
import os
from bots.utils.tests import make_character_and_state
from bots.wakeup.wakeup_actions import WakeUpActions
from bots.wakeup.wakeup_bio import WakeUpBio
from bots.wakeup.wakeup_channel import WakeUpChannel
from bots.wakeup.wakeup_conversation import WakeUpConversation
from bots.wakeup.wakeup_lore import WakeUpLore
from bots.wakeup.wakeup_style import WakeUpStyle
from bots.wakeup.wakeup_time import WakeUpTime





class TestWakeUp(unittest.TestCase):
  
  #########################################################  
  # wakeup_action
  #########################################################

  def test_actions1(self):
    character, state = make_character_and_state()
    actions = WakeUpActions().get(character, state)
    lines = actions.split('\n')
    print('<WakeUpActions>')
    print(actions)
    print('</WakeUpActions>')
    self.assertGreater(len(lines), 10)
    

    
  #########################################################  
  # wakeup_bio
  #########################################################

  def test_bio1(self):
    character, state = make_character_and_state()
    bio = WakeUpBio().get(character, state)
    print('<WakeUpBio>')
    print(bio)
    print('</WakeUpBio>')
    lines = bio.split('\n')
    self.assertEqual(len(lines), 5)




  #########################################################  
  # wakeup_channel
  #########################################################

  def test_channel1(self):
    character, state = make_character_and_state(root_parent_url='https://farcaster.group/data')
    channel = WakeUpChannel().get(character, state)
    print('<WakeUpChannel>')
    print(channel)
    print('</WakeUpChannel>')
    self.assertEqual(channel, '/data')

  def test_channel2(self):
    character, state = make_character_and_state()
    channel = WakeUpChannel().get(character, state)
    print('<WakeUpChannel>')
    print(channel)
    print('</WakeUpChannel>')
    self.assertEqual(channel, '')
    


  #########################################################
  # wakeup_conversation
  #########################################################
  
  def test_conversation1(self):
    request = "Hello World"
    character, state = make_character_and_state(request)
    conversation = WakeUpConversation().get(character, state)
    print('<WakeUpConversation>')
    print(conversation)
    print('</WakeUpConversation>')
    self.assertIn(request, conversation)

  def test_conversation2(self):
    request = "Find similar casts"
    parent_hash = '0x8fa5e35f8b843c1713a2c4d32a59edc6a2abb863'
    character, state = make_character_and_state(request=request, parent_hash=parent_hash)
    conversation = WakeUpConversation().get(character, state)
    print('<WakeUpConversation>')
    print(conversation)
    print('</WakeUpConversation>')
    self.assertIn(request, conversation)
    self.assertIn('@v', conversation)
    self.assertIn('@unknown_user', conversation)
    
  def test_conversation3(self):
    attachment_hash = '0xbe89c48299d8b080267ddd96c06c84397ee13185'
    request = "Other casts like this one?"
    character, state = make_character_and_state(request=request, attachment_hash=attachment_hash)    
    conversation = WakeUpConversation().get(character, state)
    print('<WakeUpConversation>')
    print(conversation)
    print('</WakeUpConversation>')
    self.assertIn(request, conversation)
    self.assertIn('@unknown_user', conversation)
    self.assertIn('quoting @ds007', conversation)
    self.assertIn('I like #DataScience and #ML therefore I like #Farcaster', conversation)
    
  def test_conversation4(self):
    request = "More like this"
    fid_origin = 253232
    parent_hash = '0x6f119aad7fa236cd31eeebd03d569bc264350d29'
    character, state = make_character_and_state(request=request, fid_origin=fid_origin, parent_hash=parent_hash)    
    conversation = WakeUpConversation().get(character, state)
    print('<WakeUpConversation>')
    print(conversation)
    print('</WakeUpConversation>')
    self.assertIn(request, conversation)
    self.assertIn('@horsefacts.eth', conversation)
    self.assertIn('@randombishop', conversation)
    self.assertIn('quoting @greg', conversation)
    self.assertIn('post a picture of you from a different era', conversation)

  def test_conversation5(self):
    request = "Deleted parent test"
    parent_hash = '0xb59fcfda9e859be648e5d5541d292a6fb8cc9fcb'
    character, state = make_character_and_state(request=request, parent_hash=parent_hash)    
    conversation = WakeUpConversation().get(character, state)
    print('<WakeUpConversation>')
    print(conversation)
    print('</WakeUpConversation>')
    self.assertIn(request, conversation)
    

    
  #########################################################
  # wakeup_lore
  #########################################################
  def test_lore1(self):
    character, state = make_character_and_state()
    lore = WakeUpLore().get(character, state)
    print('<WakeUpLore>')
    print(lore)
    print('</WakeUpLore>')
    lines = lore.split('\n')
    self.assertEqual(len(lines), 5)
    


  #########################################################
  # wakeup_style
  #########################################################
  def test_style1(self):
    character, state = make_character_and_state()
    style = WakeUpStyle().get(character, state)
    lines = style.split('\n')
    print('<WakeUpStyle>')
    print(style)
    print('</WakeUpStyle>')
    self.assertEqual(len(lines), 10) 
    


  #########################################################
  # wakeup_time
  #########################################################
  def test_time1(self):
    character, state = make_character_and_state()
    time = WakeUpTime().get(character, state)
    print('<WakeUpTime>')
    print(time)
    print('</WakeUpTime>')
    self.assertRegex(time, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
