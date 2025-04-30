# Data interfaces
from bots.kit_interface.most_active_users import MostActiveUsers
# Tool implementations
from bots.kit_impl.prepare.create_most_active_users_chart import create_most_active_users_chart

class Prepare:
  
  def __init__(self, state):
    self.state = state

  def create_most_active_users_chart(self, data: MostActiveUsers) -> str:
    """
    Create a chart for the most active users in a channel.
    
    Args:
        data (MostActiveUsers): The data to create the chart from.
  
    Returns:
        str: The chart image url.
    """
    return create_most_active_users_chart(data)
  