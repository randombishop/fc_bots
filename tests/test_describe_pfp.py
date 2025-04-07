from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.utils.tests import make_tool_input
from bots.tools.prepare.describe_pfp import prepare


class TestDescribePfp(unittest.TestCase):

  def _describe_pfp(self, url):
    input = make_tool_input({'user_pfp_url': url})
    result = prepare(input)
    print(result)
    self.assertTrue(len(result['user_pfp_description']) > 0)
    
  def test1(self):
    url = 'https://imagedelivery.net/BXluQx4ige9GuW0Ia56BHw/482ceb2b-91ee-4885-eb4a-02f46a08ac00/original'
    self._describe_pfp(url)
    
  def test2(self):
    url = 'https://imagedelivery.net/BXluQx4ige9GuW0Ia56BHw/969839fe-ab1c-4a8d-c849-062737f06e00/original'
    self._describe_pfp(url)
    
    
    
    
  