# Data interfaces
from bots.kit_interface.image_description import ImageDescription
from bots.kit_interface.user_profile import UserProfile
from bots.kit_interface.user_casts_description import UserCastsDescription
from bots.kit_interface.user_reactions_description import UserReactionsDescription
from bots.kit_interface.user_id import UserId
from bots.kit_interface.avatar import Avatar
# Tool implementations
from bots.kit_impl.memorize.save_user_profile import save_user_profile


class Memorize:
  
  def __init__(self, state):
    self.state = state

  def save_user_profile(self, user_id: UserId, user_profile: UserProfile, pfp_description: ImageDescription, casts_description: UserCastsDescription, reactions_description: UserReactionsDescription, avatar: Avatar ) -> str:
    """
    Save the user profile in long term memory.
    
    Args:
        user_id (UserId): The user's id.
        user_profile (UserProfile): The user's profile.
        pfp_description (ImageDescription): The description of the user's profile picture.
        casts_description (UserCastsDescription): The description of the user's casts.
        reactions_description (UserReactionsDescription): The description of the user's replies and reactions.
        avatar (Avatar): The avatar of the user.
        
    Returns:
        str: Status log of the save operation.
    """
    return save_user_profile(user_id, user_profile, pfp_description, casts_description, reactions_description, avatar)
  
  