class Cast:
  """
  Represents a farcaster cast (cast=post).
  """
  
  def __init__(self, data: dict):
    self.id = data['hash'][2:8]
    self.hash = data['hash']
    self.fid = data['fid']
    self.username = data['username']
    self.text = data['text']
    self.mentions = data['mentions'] if 'mentions' in data else []
    self.mentionsPos = data['mentionsPos'] if 'mentionsPos' in data else []
    self.parent_fid = data['parent_fid'] if 'parent_fid' in data else None
    self.parent_hash = data['parent_hash'] if 'parent_hash' in data else None
    self.parent_cast = Cast(data['parent_cast']) if 'parent_cast' in data else None
    self.timestamp = data['timestamp']
    self.when = data['when']  
    
  def __str__(self) -> str:
    ans = f"<{self.id}>\n"
    ans += f"@{self.username} said ({self.when}):\n{self.text}\n"
    if self.parent_cast is not None:
      ans += f"[Replying to @{self.parent_cast.username}: {self.parent_cast.text}]\n"
    ans += f"</{self.id}>\n"
    return ans