from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestChat(unittest.TestCase):

  def assert_expected_output(self, bot, expected_continue):
    action = bot.state.selected_action
    if expected_continue:
      self.assertTrue(action == 'Chat')
      self.assertEqual(len(bot.state.casts), 1)
      self.assertTrue(bot.state.reply)
    else:
      self.assertTrue(action is None or action == 'Chat')
      self.assertEqual(len(bot.state.casts), 0)
      self.assertFalse(bot.state.reply)    
  
  
  
  def test1(self):
    request = "Not interested."
    bot = run_bot(request)
    self.assert_expected_output(bot, False)

  def test2(self):
    request = "Chat with me: Who are you?"
    bot = run_bot(request)
    self.assert_expected_output(bot, True)

  def test3(self):
    request = "Chat with me: Do you think DeepSeek will surpass OpenAI?"
    fid_origin=253232
    bot = run_bot(request, fid_origin=fid_origin)
    self.assert_expected_output(bot, True)

  def test4(self):
    request = "Thank you so much for sharing 😺❤️❤️❤️"
    fid_origin=388401
    parent_hash='0x7506e607e722d543b61306d1357814ad61caa132'
    bot = run_bot(request, fid_origin=fid_origin, parent_hash=parent_hash)
    self.assert_expected_output(bot, False)