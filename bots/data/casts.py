from datetime import datetime, timedelta
from google.cloud import bigquery
from bots.data.bq import execute
from bots.data.pg import pg_connection


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


def get_cast(hash):
  hash = hash.replace('0x', '')
  sql = f"""
  select fid,
  body->>'text' as text,
  (body->'parent'->>'fid')::INTEGER as parent_fid,
  body->'parent'->>'hash' as parent_hash
  from messages
  where hash = '\\x{hash}'::bytea;
  """
  with pg_connection.cursor() as cursor:
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is not None:
      return {
        'fid': row[0],
        'text': row[1],
        'parent_fid': row[2],
        'parent_hash': row[3]
      }
    else:
      return None
  