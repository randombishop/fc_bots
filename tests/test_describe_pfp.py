from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_tool_input
from bots.tools.prepare.describe_pfp import prepare


class TestDescribePfp(unittest.TestCase):

  def test1(self):
    url = 'https://imgur.com/tABKvo7'
    input = make_tool_input({'user_pfp_url': url})
    result = prepare(input)
    print(result)
    
    
    
    
  