from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import run_agent


class TestBlueprints(unittest.TestCase):
      
  def test1(self):
    state = run_agent(
      test_id='TestBlueprints:test1',
      mode='blueprint',
      blueprint='WhoIs',
      user='randombishop'
    )
    self.assertTrue(state.has_variable_value_with_type('Avatar'))
    
  