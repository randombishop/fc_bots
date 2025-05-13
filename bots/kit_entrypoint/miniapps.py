# Data interfaces
from bots.kit_interface.miniapp import MiniApp
from bots.kit_interface.user_id import UserId
# Tool implementations
from bots.kit_impl.miniapp.avatar_match import get_avatar_match


class MiniApps:
  
  def __init__(self, state):
    self.state = state    

  def get_avatar_match(self, user_id: UserId) -> MiniApp:
    """     
    Get a mini-app for the avatar match mini-app.
    This app shows the user's avatar and profile and lets them play a matching game, find similar profiles, and also mint their own NFT. 
    
    Args:
        user_id (UserId): The user id to cutomize the mini-app splash screen.  
  
    Returns:
        MiniApp: The mini-app url.
    """
    return get_avatar_match(user_id)
