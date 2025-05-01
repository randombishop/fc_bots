# Data interfaces
from bots.kit_interface.most_active_users import MostActiveUsers
from bots.kit_interface.word_cloud_data import WordCloudData
from bots.kit_interface.word_cloud_mask import WordCloudMask
from bots.kit_interface.casts import Casts
from bots.kit_interface.favorite_users import FavoriteUsers
from bots.kit_interface.favorite_users_table import FavoriteUsersTable
from bots.kit_interface.most_active_users_chart import MostActiveUsersChart
from bots.kit_interface.word_cloud_image import WordCloudImage
from bots.kit_interface.image_description import ImageDescription
from bots.kit_interface.user_profile import UserProfile
# Tool implementations
from bots.kit_impl.prepare.create_most_active_users_chart import create_most_active_users_chart
from bots.kit_impl.prepare.make_word_cloud_data import make_word_cloud_data
from bots.kit_impl.prepare.make_word_cloud_mask import make_word_cloud_mask
from bots.kit_impl.prepare.render_favorite_users_table import render_favorite_users_table
from bots.kit_impl.prepare.create_wordcloud import create_wordcloud
from bots.kit_impl.prepare.describe_pfp import describe_pfp


class Prepare:
  
  def __init__(self, state):
    self.state = state

  def create_most_active_users_chart(self, data: MostActiveUsers) -> MostActiveUsersChart:
    """
    Create a chart for the most active users in a channel.
    
    Args:
        data (MostActiveUsers): The data to create the chart from.
  
    Returns:
        MostActiveUsersChart: The chart image url.
    """
    return create_most_active_users_chart(data)
  
  def render_favorite_users_table(self, data: FavoriteUsers) -> FavoriteUsersTable:
    """
    Render a table for the favorite users in a channel.
    
    Args:
        data (FavoriteUsers): The data to render the table from.  
  
    Returns:
        FavoriteUsersTable: The table image url.
    """
    return render_favorite_users_table(data)
  
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
  
  def create_wordcloud(self, data: WordCloudData, mask: WordCloudMask) -> WordCloudImage:
    """
    Create a word cloud image.
    
    Args:
        data (WordCloudData): The data containing the word counts.  
        mask (WordCloudMask): The word cloud mask and background.
  
    Returns:
        WordCloudImage: The word cloud image url.
    """
    return create_wordcloud(data, mask)
  
  def describe_pfp(self, user_profile: UserProfile) -> ImageDescription:
    """
    Describe a user's profile picture.
    
    Args:
        user_profile (UserProfile): The user's profile containing the target pfp_url. 
  
    Returns:
        ImageDescription: The description of the image.
    """
    return describe_pfp(user_profile)
  
  
  