from dotenv import load_dotenv
load_dotenv()
import unittest
from bots.kit_interface.user_info import UserInfo
from bots.kit_impl.prepare.describe_pfp import describe_pfp


class TestDescribePfp(unittest.TestCase):

  def _describe_pfp(self, url):
    user_profile = UserInfo('Name', 'bio', 0, 0, url)
    image_description = describe_pfp(user_profile)
    print(image_description)
    self.assertTrue(len(image_description.description) > 0)
    
  def test1(self):
    url = 'https://imagedelivery.net/BXluQx4ige9GuW0Ia56BHw/482ceb2b-91ee-4885-eb4a-02f46a08ac00/original'
    self._describe_pfp(url)
    
  def test2(self):
    url = 'https://imagedelivery.net/BXluQx4ige9GuW0Ia56BHw/969839fe-ab1c-4a8d-c849-062737f06e00/original'
    self._describe_pfp(url)
    
    
    
    
  