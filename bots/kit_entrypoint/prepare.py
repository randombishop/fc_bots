# Data interfaces
from bots.kit_interface.avatar import Avatar
from bots.kit_interface.casts import Casts
from bots.kit_interface.favorite_users import FavoriteUsers
from bots.kit_interface.favorite_users_table import FavoriteUsersTable
from bots.kit_interface.image import Image
from bots.kit_interface.image_description import ImageDescription
from bots.kit_interface.most_active_users import MostActiveUsers
from bots.kit_interface.most_active_users_chart import MostActiveUsersChart
from bots.kit_interface.reactions import Reactions
from bots.kit_interface.user_casts_description import UserCastsDescription
from bots.kit_interface.user_id import UserId
from bots.kit_interface.user_profile import UserProfile
from bots.kit_interface.user_reactions_description import UserReactionsDescription
from bots.kit_interface.word_cloud_data import WordCloudData
from bots.kit_interface.word_cloud_image import WordCloudImage
from bots.kit_interface.word_cloud_mask import WordCloudMask
# Tool implementations
from bots.kit_impl.prepare.create_avatar import create_avatar
from bots.kit_impl.prepare.create_image import create_image
from bots.kit_impl.prepare.create_most_active_users_chart import create_most_active_users_chart
from bots.kit_impl.prepare.create_wordcloud import create_wordcloud
from bots.kit_impl.prepare.describe_pfp import describe_pfp
from bots.kit_impl.prepare.describe_user_casts import describe_user_casts
from bots.kit_impl.prepare.describe_user_reactions import describe_user_reactions
from bots.kit_impl.prepare.make_word_cloud_data import make_word_cloud_data
from bots.kit_impl.prepare.make_word_cloud_mask import make_word_cloud_mask
from bots.kit_impl.prepare.render_favorite_users_table import render_favorite_users_table
# utils
from bots.utils.format_state import format_state


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
  
  def make_word_cloud_data(self, casts: Casts) -> WordCloudData:
    """
    Create a data object before rendering a word cloud.
    
    Args:
        casts (Casts): The list of casts to prepare the word cloud data.
  
    Returns:
        WordCloudData: Text and word counts.
    """
    return make_word_cloud_data(casts)
  
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
  
  def describe_user_casts(self, user_id: UserId, user_profile: UserProfile, casts: Casts) -> UserCastsDescription:
    """
    Describe a user's casts.
    
    Args:
        user_id (UserId): The user's id.  
        user_profile (UserProfile): The user's profile.
        casts (Casts): The user's casts.
  
    Returns:
        UserCastsDescription: The description of the user's casts.
    """
    return describe_user_casts(bot_name=self.state.bot_name, 
                               bio=self.state.get_variable('bio').value, 
                               lore=self.state.get_variable('lore').value,
                               style=self.state.get_variable('style').value,
                               user_id=user_id,
                               user_profile=user_profile,
                               casts=casts)
  
  def describe_user_reactions(self, user_id: UserId, user_profile: UserProfile, reactions: Reactions) -> UserReactionsDescription:
    """
    Describe a user's replies and reactions.
    
    Args:
        user_id (UserId): The user's id.  
        user_profile (UserProfile): The user's profile.
        reactions (list[Reaction]): The user's reactions.
  
    Returns:
        UserReactionsDescription: The description of the user's replies and reactions.
    """
    return describe_user_reactions(bot_name=self.state.bot_name, 
                                    bio=self.state.get_variable('bio').value, 
                                    lore=self.state.get_variable('lore').value,
                                    style=self.state.get_variable('style').value,
                                    user_id=user_id,
                                    user_profile=user_profile,
                                    reactions=reactions) 
  
  def create_avatar(self, user_id: UserId, user_profile: UserProfile, pfp_description: ImageDescription, casts_user: Casts, casts_description: UserCastsDescription) -> Avatar:
    """
    Create an avatar for a user.
    
    Args:
        user_id (UserId): The user's id.  
        user_profile (UserProfile): The user's profile.
        pfp_description (ImageDescription): The description of the user's profile picture.
        casts_user (Casts): The user's casts.
        casts_description (UserCastsDescription): The description of the user's casts.
  
    Returns:
        Avatar: The avatar image url.
    """
    return create_avatar(bot_name=self.state.bot_name,   
                         bio=self.state.get_variable('bio').value, 
                         lore=self.state.get_variable('lore').value,
                         user_id=user_id,
                         user_profile=user_profile,
                         pfp_description=pfp_description,
                         casts=casts_user,
                         casts_description=casts_description) 
  
  def create_image(self) -> Image:
    """
    Create an image based on current context.
    Use this method when you need to create a new image for your post. 
    It will generate a prompt and then use dall-e3 to generate an image.
    Avoid calling this method in the beginning of your tool sequences, use it rather towards the end to make sure it has all the context it needs.
    
    Returns:
        Image: The image url.
    """
    return create_image(context=format_state(self.state, intro=True, variables=True), 
                        bot_name=self.state.bot_name, 
                        bio=self.state.get_variable('bio').value, 
                        lore=self.state.get_variable('lore').value)