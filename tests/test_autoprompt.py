from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_bot


class TestAutoprompt(unittest.TestCase):
      
  
  def test1(self):
    state = run_bot(test_id='TestAutoprompt:test1', channel='mfers', action='MostActiveUsers')
    self.assertIn('The most active mfers are',state.casts[0]['text'])
    
  def test2(self):
    state = run_bot(test_id='TestAutoprompt:test2', action='WhoIs', user='randombishop')
    self.assertEquals(state.casts[0]['mentions'][0], 253232)
      
  def test3(self):
    state = run_bot(test_id='TestAutoprompt:test3', channel='product', action='Summary')
    self.assertEquals(len(state.casts), 3)
    self.assertEquals(len(state.casts[0]['embeds']), 1)
  