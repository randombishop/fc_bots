class Conversation:
  """
  Stores the context's conversation.
  """
  
  def __init__(self, conversation: str):
    self.conversation = conversation
      
  def __str__(self) -> str:
    return f"#CONVERSATION\n{self.conversation}"  