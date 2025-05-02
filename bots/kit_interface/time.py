import datetime


class Time:
  """
  Current date and time.
  """
  
  def __init__(self):
    self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
      
  def __str__(self) -> str:
    return self.time