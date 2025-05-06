import pandas

class DataFrame:
  """
  Represents a pandas dataframe resulting from a SQL query or an API call.
  """
  
  def __init__(self, df: pandas.DataFrame):
    self.df = df
      
  def __str__(self) -> str:
    return self.df.to_string(index=False)
  
