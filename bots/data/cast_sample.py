import os
from datetime import datetime, timedelta
from google.cloud import bigquery
from bots.data.bq import bq_client, dataset_id


sql_select = """
SELECT  
t.timestamp,
t.hash,
t.fid,
t.user_name,
t.text
FROM `cast_features` t
"""


sql_order_by_engagement = """
ORDER BY (
(predict_like/100)
+ (2 * IFNULL(h12_likes, 0))
+ (3 * IFNULL(h12_recasts, 0)) 
+ (1 * IFNULL(h12_replies, 0)) 
) DESC
"""


def make_sql(channel, num_days, max_rows, keywords, order_by):
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
  sql += order_by
  sql += f"LIMIT {max_rows}"
  return sql, params


def get_casts_with_top_engagement(channel, num_days, max_rows, keywords):
  sql, params = make_sql(channel, num_days, max_rows, keywords, sql_order_by_engagement)
  job_config = bigquery.QueryJobConfig(default_dataset=dataset_id, query_parameters=params)
  query_job = bq_client.query(sql, job_config)
  results = [x for x in query_job.result()]
  return results