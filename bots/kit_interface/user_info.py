class UserInfo:
  """
  Represents a farcaster user's basic information.
  """
  
  def __init__(self, display_name: str, bio: str, followers: int, following: int, pfp_url: str):
    self.display_name = display_name
    self.bio = bio
    self.followers = followers
    self.following = following
    self.pfp_url = pfp_url
      
  def __str__(self) -> str:
    ans = f"display_name: {self.display_name}\n"
    ans += f"bio: {self.bio}\n"
    ans += f"followers: {self.followers}\n"
    ans += f"following: {self.following}\n"
    ans += f"pfp_url: {self.pfp_url}\n"
    return ans