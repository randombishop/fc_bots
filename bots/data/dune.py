from dune_client.client import DuneClient
from dune_client.query import QueryBase
import logging
logging.getLogger("dune_client.api.base").setLevel(logging.WARNING)


dune = DuneClient.from_env()


def run_query(query_id, params=None):
  print(f"Running Dune query {query_id}...")
  if params is not None and len(params) > 0:
    for p in params[:10]:
      print(f"  {p.key}: {p.value}")
  query = QueryBase(query_id=query_id, params=params)
  df = dune.run_query_dataframe(query)
  if df is not None and df.shape[0] > 0:
    print(f"  {df.shape[0]} rows returned.")
  else:
    print("  No rows returned.")
  return df

def to_array(result):
  values = [x.values() for x in result]
  columns = list(result[0].keys())
  return {'values': values, 'columns': columns}