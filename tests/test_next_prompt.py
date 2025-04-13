from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.next_prompt import get_next_prompt


class TestNextPrompt(unittest.TestCase):
  
  def test1(self):
    next = get_next_prompt(788096)
    print('TestNextPrompt:test1')
    print(next)
    self.assertIsNotNone(next['prompt_id'])
    self.assertIsNotNone(next['channel'])
    
  def test2(self):
    next = get_next_prompt(253232)
    print('TestNextPrompt:test2')
    print(next)
    self.assertIsNotNone(next['prompt_id'])
    self.assertIsNotNone(next['channel'])
    