import os
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest


project_id = os.environ['GCP_PROJECT_ID']
dataset_id = project_id + '.' + os.environ['GCP_DATASET_ID']
bq_client = bigquery.Client(project=project_id)

def dry_run(sql):
  try:
    job_config = bigquery.QueryJobConfig(
      default_dataset=dataset_id,
      dry_run=True,
      use_query_cache=False)
    query_job = bq_client.query(sql, job_config=job_config)
    total_bytes_processed = int(query_job.total_bytes_processed) if query_job.total_bytes_processed else 0
    estimated_bytes_processed = int(query_job.estimated_bytes_processed) if query_job.estimated_bytes_processed else 0
    cost = int(max(total_bytes_processed, estimated_bytes_processed)/1000000)
    ans = {
      'total_bytes_processed': query_job.total_bytes_processed,
      'estimated_bytes_processed': query_job.estimated_bytes_processed,
      'clustering_fields': query_job.clustering_fields,
      'cost': cost
    }
    if query_job.errors:
      ans['error'] = query_job.errors
    return ans
  except BadRequest as e:
    return {'error': e.errors}
  except Exception as e:
    return {'error': e.message}
