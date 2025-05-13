from bots.kit_interface.cast import Cast


class Casts:
  """
  Represents a list of farcaster casts (casts=posts).
  """
  
  def __init__(self, description: str, data: list[Cast]):
    self.description = description
    self.casts = data
      
  def __str__(self) -> str:
    ans = f"#{self.description}\n"
    if len(self.casts) > 0:
      for cast in self.casts:
        ans += f"{cast}\n"
    else:
      ans += "No casts found.\n"
    return ans