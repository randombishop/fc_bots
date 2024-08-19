import os
from datetime import datetime, timedelta
from google.cloud import bigquery
from bots.data.bq import bq_client, dataset_id


sql_select = """
SELECT 
target_fid, 
(select user_name from `deep-mark-425321-r7`.dsart_farcaster.fid_username where fid_username.fid=reactions.target_fid) as username,
num_recasts, 
num_likes, 
num_replies 
FROM `deep-mark-425321-r7`.dsart_farcaster.reactions 
WHERE fid={} and target_fid!={}
ORDER BY (3*num_recasts + 2*num_likes + 1*num_replies) DESC
LIMIT 10 ;
"""


def favorite_users_sql(fid):
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
  job_config = bigquery.QueryJobConfig(default_dataset=dataset_id, query_parameters=params)
  query_job = bq_client.query(sql, job_config)
  results = [x for x in query_job.result()]
  return results