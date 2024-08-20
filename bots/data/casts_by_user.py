from datetime import datetime, timedelta
from google.cloud import bigquery
from bots.data.bq import bq_client, dataset_id



def casts_by_user_sql(channel, num_days, max_rows):
  today = datetime.today()
  days = [(today + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(-(num_days+1), 1)]
  sql = 'SELECT user_name, \n'
  for day in days:
    sql += f"SUM(CASE WHEN day = '{day}' THEN 1 ELSE 0 END) AS `casts-{day}`, \n"
  sql += "count(*) as casts_total \n"
  sql += 'FROM cast_features \n'
  sql += f"WHERE (day > '{days[0]}') \n"
  sql += f"AND (day < '{days[-1]}') \n"
  sql += f"AND (parent_url = '{channel}') \n"
  sql += "AND user_name is not null \n"
  sql += "GROUP BY user_name \n"
  sql += "ORDER BY casts_total DESC \n"
  sql += f"LIMIT {max_rows}"
  return sql


def casts_by_user_results(channel, num_days, max_rows):
  sql = casts_by_user_sql(channel, num_days, max_rows)
  job_config = bigquery.QueryJobConfig(default_dataset=dataset_id)
  query_job = bq_client.query(sql, job_config)
  results = [x for x in query_job.result()]
  return results