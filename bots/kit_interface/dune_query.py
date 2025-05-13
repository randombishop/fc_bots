class DuneQuery:
  """
  Represents a SQL query to call Dune Analytics (Trino SQL dialect).
  """
  
  def __init__(self, sql: str):
    self.sql = sql
      
  def __str__(self) -> str:
    return self.sql
  
