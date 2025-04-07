from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_tool_input
from bots.tools.prepare.describe_pfp import prepare


class TestDescribePfp(unittest.TestCase):

  def test1(self):
    url = 'https://imagedelivery.net/BXluQx4ige9GuW0Ia56BHw/b5367417-4f80-405e-e5a9-22131232d800/original'
    input = make_tool_input({'user_pfp_url': url})
    result = prepare(input)
    print(result)
    
    
    
    
  