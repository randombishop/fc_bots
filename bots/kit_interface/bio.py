from bots.utils.format_character import format_bio


class Bio:
  """
  Stores the bot's bio.
  """
  
  def __init__(self, bio: list[str]):
    self.bio = bio
      
  def __str__(self) -> str:
    return format_bio(self.bio) 