from dotenv import load_dotenv
load_dotenv()
import os
import unittest
from bots.data.app import get_bot_character


bot_id = int(os.getenv('TEST_BOT'))


class TestCharacter(unittest.TestCase):
  
  def test1(self):
    character = get_bot_character(bot_id)
    # Check that bot has some data
    self.assertIsInstance(character['name'], str)
    self.assertIsInstance(character['bio'], list)
    self.assertIsInstance(character['lore'], list)
    self.assertIsInstance(character['style'], list)

    
