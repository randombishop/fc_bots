from google.cloud import bigquery
from bots.data.bq import bq_client, dataset_id


fav_usr_sql = """
SELECT 
target_fid, 
(select user_name from fid_username where fid_username.fid=reactions.target_fid) as username,
num_recasts, 
num_likes, 
num_replies 
FROM reactions 
WHERE fid={} and target_fid!={}
ORDER BY (3*num_recasts + 2*num_likes + 1*num_replies) DESC
LIMIT 10 ;
"""

def favorite_users_sql(fid):
  return fav_usr_sql.format(fid, fid)

def favorite_users_results(fid):
  sql = favorite_users_sql(fid)
  job_config = bigquery.QueryJobConfig(default_dataset=dataset_id)
  query_job = bq_client.query(sql, job_config)
  results = [x for x in query_job.result()]
  return results