import pandas


class FavoriteUsers:
  """
  Data frame containing the favorite accounts of a user and their engagement counts with them.
  """
  
  def __init__(self, df: pandas.DataFrame):
    self.df = df
      
  def __str__(self) -> str:
    return f"#FavoriteUsers:\n{self.df.to_string(index=False)}"  