from dune_client.client import DuneClient
from dune_client.query import QueryBase


dune = DuneClient.from_env()


def run_query(query_id, params=None):
  print(f"Running Dune query {query_id} with params {params}")
  query = QueryBase(query_id=query_id, params=params)
  df = dune.run_query_dataframe(query)
  return df

def to_array(result):
  values = [x.values() for x in result]
  columns = list(result[0].keys())
  return {'values': values, 'columns': columns}