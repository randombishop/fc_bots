from datetime import datetime, timedelta
from google.cloud import bigquery
from bots.data.bq import execute


def text_for_fid_sql(fid, num_days):
  params = []
  today = datetime.today()
  past = (today - timedelta(days=(num_days+1))).strftime("%Y-%m-%d")
  sql = """
  SELECT text
  FROM cast_features
  WHERE day > ?
  AND fid = ?
  ORDER BY timestamp DESC
  LIMIT 100
  """
  params.append(bigquery.ScalarQueryParameter(None, "DATE", past))
  params.append(bigquery.ScalarQueryParameter(None, "INTEGER", fid))
  return sql, params


def text_for_fid_results(fid, num_days):
  sql, params = text_for_fid_sql(fid, num_days)
  response = execute(sql, params)
  results = [x['text'] for x in response]
  return results