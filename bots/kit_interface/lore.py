from bots.utils.format_character import format_lore


class Lore:
  """
  Stores the bot's lore.
  """
  
  def __init__(self, lore: list[str]):
    self.lore = lore
      
  def __str__(self) -> str:
    return f"#LORE\n{format_lore(self.lore)}"  