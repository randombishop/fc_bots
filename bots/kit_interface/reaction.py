from bots.kit_interface.cast import Cast
from bots.utils.format_cast import shorten_text


class Reaction:
  """
  Represents a farcaster reaction: like, recast or reply.
  """
  
  def __init__(self, data: dict):
    self.type = data['type']
    self.timestamp = data['timestamp']
    self.when = data['when']  
    self.cast = Cast(data['cast'])
    
  def __str__(self) -> str:
    text = ''
    if self.type == 'reply' and self.cast.parent_cast is not None:
      text += f"✉️ Replied\n"
      text += f"@{self.cast.parent_cast.username} said: {shorten_text(self.cast.parent_cast.text)}\n"
      text += f"@{self.cast.username} replied: {self.cast.text}\n"
      text += '\n'
    elif self.type == 'like':
      text += "❤️ Liked "
      text += f"@{self.cast.username}'s cast: "
      text += f"@{shorten_text(self.cast.text)}\n"
      text += '\n'
    elif self.type == 'recast':
      text += "🔁 Reposted "
      text += f"@{self.cast.username}'s cast: "
      text += f"@{shorten_text(self.cast.text)}\n"
      text += '\n'
    else:
      text += f"* {self.type} *\n"
      text += '\n'
    return text