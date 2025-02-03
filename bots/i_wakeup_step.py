class IWakeUpStep:
    
  def get(self, bot_character, bot_state):
    """Return the associated casts."""
    raise NotImplementedError("Action doesn't implement get_casts")
  