from bots.kit_interface.reaction import Reaction


class Reactions:
  """
  Represents a list of farcaster reactions (likes, recasts and replies).
  """   
  
  def __init__(self, data: list[Reaction]):
    self.reactions = data
      
  def __str__(self) -> str:
    if len(self.reactions) > 0:
      return "\n".join([str(reaction) for reaction in self.reactions])
    else:
      return "No reactions found.\n"