import logging
import time
from dune_client.client import DuneClient
from dune_client.query import QueryBase
logging.getLogger("dune_client.api.base").setLevel(logging.WARNING)


dune = None
try:
  dune = DuneClient.from_env()
except Exception as e:
  print("Warning: Dune client is not available.")

def run_query(query_id, params=None):
  t0 = time.time()
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
  print(f"  Time: {time.time() - t0:.2f} seconds")
  return df


def to_array(result):
  values = [x.values() for x in result]
  columns = list(result[0].keys())
  return {'values': values, 'columns': columns}


def run_sql(sql):
  t0 = time.time()
  print(f"Running Dune custom SQL:\n{sql}")
  create_response = dune.create_query(
    name="Temp",
    query_sql=sql,
    is_private=True
  )
  query_id = create_response.base.query_id
  try:
    query = QueryBase(query_id=query_id)
    df = dune.run_query_dataframe(query)
    if df is not None and df.shape[0] > 0:
      print(f"  {df.shape[0]} rows returned.")
    else:
      print("  No rows returned.")
    print(f"  Time: {time.time() - t0:.2f} seconds")
    return df
  finally:
    dune.archive_query(query_id)