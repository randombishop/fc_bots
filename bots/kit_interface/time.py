import datetime


class Time:
  """
  Current date and time.
  """
  
  def __init__(self):
    self.time = datetime.now().strftime('%Y-%m-%d %H:%M')
      
  def __str__(self) -> str:
    return f"#CURRENT TIME: {self.time}"  