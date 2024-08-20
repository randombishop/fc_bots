from datetime import datetime, timedelta
from google.cloud import bigquery
from bots.data.bq import execute


sql_select = """
SELECT  
t.timestamp,
t.hash,
t.fid,
t.user_name,
t.text
FROM cast_features t
"""


sql_order = """
ORDER BY (
(predict_like/100)
+ (2 * IFNULL(h12_likes, 0))
+ (3 * IFNULL(h12_recasts, 0)) 
+ (1 * IFNULL(h12_replies, 0)) 
) DESC
"""


def top_casts_sql(channel, num_days, max_rows, keywords):
  params = []
  sql = sql_select
  today = datetime.today()
  past = (today - timedelta(days=(num_days+1))).strftime("%Y-%m-%d")
  sql += "WHERE day > ? \n"
  sql += "AND t.parent_fid = -1 \n"
  sql += "AND q_info>50 \n"
  params.append(bigquery.ScalarQueryParameter(None, "DATE", past))
  if channel is None:
    sql += "AND (t.parent_url is NULL) \n"
  else:
    sql += "AND (t.parent_url = ?) \n"
    params.append(bigquery.ScalarQueryParameter(None, "STRING", channel))
  if keywords is not None and len(keywords) > 0:
    conditions = ["(LOWER(text) LIKE ?)" for _ in keywords]
    params += [bigquery.ScalarQueryParameter(None, "STRING", f"%{keyword}%") for keyword in keywords]
    sql += "AND (" + " OR ".join(conditions) + ") \n"
  sql += sql_order
  sql += f"LIMIT {max_rows}"
  return sql, params


def top_casts_results(channel, num_days, max_rows, keywords):
  sql, params = top_casts_sql(channel, num_days, max_rows, keywords)
  response = execute(sql, params)
  results = [x for x in response]
  return results