from bots.kit_interface.dune_query import DuneQuery
from bots.kit_interface.data_frame import DataFrame
from bots.data.dune import run_sql


def execute_dune_query(query: DuneQuery) -> DataFrame:
  df = run_sql(query.sql)    
  return DataFrame(df)

