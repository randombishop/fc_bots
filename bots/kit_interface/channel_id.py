class ChannelId:
  """
  Represents a Farcaster channel identifier.
  """
  
  def __init__(self, channel: str, channel_url: str):
    self.channel = channel
    self.channel_url = channel_url
      
  def __str__(self) -> str:
    return f"#ChannelId:\n{self.channel}"