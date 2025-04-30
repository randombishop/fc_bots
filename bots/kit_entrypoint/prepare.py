# Data interfaces
from bots.kit_interface.most_active_users import MostActiveUsers
from bots.kit_interface.word_cloud_data import WordCloudData
from bots.kit_interface.word_cloud_mask import WordCloudMask
from bots.kit_interface.casts import Casts
# Tool implementations
from bots.kit_impl.prepare.create_most_active_users_chart import create_most_active_users_chart
from bots.kit_impl.prepare.make_word_cloud_data import make_word_cloud_data
from bots.kit_impl.prepare.make_word_cloud_mask import make_word_cloud_mask
class Prepare:
  
  def __init__(self, state):
    self.state = state

  def create_most_active_users_chart(self, data: MostActiveUsers) -> str:
    """
    Create a chart for the most active users in a channel.
    
    Args:
        data (MostActiveUsers): The data to create the chart from.
  
    Returns:
        str: The chart image url.
    """
    return create_most_active_users_chart(data)
  
  def make_word_cloud_data(self, data: Casts) -> WordCloudData:
    """
    Create a data object before rendering a word cloud.
    
    Args:
        data (Casts): The list of casts to prepare the word cloud data.
  
    Returns:
        WordCloudData: Text and word counts.
    """
    return make_word_cloud_data(data)
  
  def make_word_cloud_mask(self, data: WordCloudData) -> WordCloudMask:
    """
    Create a mask before rendering a word cloud.
    
    Args:
        data (WordCloudData): The data containing the word counts.  
  
    Returns:
        WordCloudMask: The word cloud mask.
    """
    return make_word_cloud_mask(data)
  
  