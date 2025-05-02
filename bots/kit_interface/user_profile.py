class UserProfile:
  """
  Represents a farcaster user profile basic information.
  """
  
  def __init__(self, display_name: str, bio: str, followers: int, following: int, pfp_url: str):
    self.display_name = display_name
    self.bio = bio
    self.followers = followers
    self.following = following
    self.pfp_url = pfp_url
      
  def __str__(self) -> str:
    return f"""
    display_name: {self.display_name}
    bio: {self.bio}
    followers: {self.followers}
    following: {self.following}
    pfp_url: {self.pfp_url}"""