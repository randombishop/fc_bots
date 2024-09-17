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
JOIN fid_features users on t.fid = users.fid and users.spam_any = 0
"""


sql_order = """
ORDER BY (
(3 * IFNULL(h12_recasts, 0))
+ (2 * IFNULL(h12_likes, 0))
+ (1 * IFNULL(h12_replies, 0)) 
) DESC
"""


def top_casts_sql(channel, num_days, max_rows, keywords, category, informative):
  params = []
  sql = sql_select
  today = datetime.today()
  past = (today - timedelta(days=(num_days+1))).strftime("%Y-%m-%d")
  sql += "WHERE t.day > ? \n"
  params.append(bigquery.ScalarQueryParameter(None, "DATE", past))
  sql += "AND t.parent_fid = -1 \n"
  if informative:
    sql += "AND q_info>50 \n"
  if category is not None:
    sql += "AND (t.category_label = ?) \n"
    params.append(bigquery.ScalarQueryParameter(None, "STRING", category))
  if channel is not None:
    sql += "AND (t.parent_url = ?) \n"
    params.append(bigquery.ScalarQueryParameter(None, "STRING", channel))
  if keywords is not None and len(keywords) > 0:
    conditions = ["(LOWER(text) LIKE ?)" for _ in keywords]
    params += [bigquery.ScalarQueryParameter(None, "STRING", f"%{keyword}%") for keyword in keywords]
    sql += "AND (" + " AND ".join(conditions) + ") \n"
  sql += sql_order
  sql += f"LIMIT {max_rows}"
  return sql, params


def top_casts_results(channel, num_days, max_rows, keywords, category, informative):
  sql, params = top_casts_sql(channel, num_days, max_rows, keywords, category, informative)
  response = execute(sql, params)
  results = [x for x in response]
  return results