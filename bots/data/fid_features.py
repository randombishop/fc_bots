import json
from bots.data.bq import bigquery, execute


def get_words_dict_sql(fid):
  sql = 'SELECT words_dict from fid_features where fid=?'
  return sql, [bigquery.ScalarQueryParameter(None, "INTEGER", fid)]


def get_words_dict(fid):
  sql, params = get_words_dict_sql(fid)
  response = execute(sql, params)
  rows = [x for x in response]
  if len(rows) == 0:
    return None
  else:
    s = rows[0]['words_dict']
    if s is None:
      return None
    else:
      return json.loads(s)

