class Cast:
  """
  Represents a farcaster cast (cast=post).
  """
  
  def __init__(self, data: dict):
    self.id = '0x' + data['hash'][2:8]
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
    self.num_likes = data['num_likes'] if 'num_likes' in data else None
    self.num_recasts = data['num_recasts'] if 'num_recasts' in data else None
    self.num_replies = data['num_replies'] if 'num_replies' in data else None
    

  def _reactions(self):
    reactions = []
    if self.num_likes is not None and self.num_likes > 0:
      reactions.append(f'{self.num_likes} ❤️')
    if self.num_recasts is not None and self.num_recasts > 0:
      reactions.append(f'{self.num_recasts} 🔁')
    if self.num_replies is not None and self.num_replies > 0:
      reactions.append(f'{self.num_replies} ✉️')
    return reactions
  
  def __str__(self) -> str:
    ans = f"<{self.id}>\n"
    ans += f"@{self.username} said ({self.when}):\n{self.text}\n"
    if self.parent_cast is not None:
      ans += f"[Replying to @{self.parent_cast.username}: {self.parent_cast.text}]\n"
    reactions = self._reactions()
    if len(reactions) > 0:
      ans += f"| {' | '.join(reactions)} |\n"
    ans += f"</{self.id}>\n"
    return ans