import os
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest


project_id = os.environ['GCP_PROJECT_ID']
dataset_id = project_id + '.' + os.environ['GCP_DATASET_ID']
dataset_tmp = project_id + '.' + os.environ['GCP_DATASET_TMP']
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
    return {'error': str(e)}


def sql_to_gcs(sql, folder, filename):
  try:
    tmp_table = f"{dataset_tmp}.{filename}"
    bucket_name = os.environ['GCP_BOT_BUCKET']
    destination_uri = f"gs://{bucket_name}/{folder}/{filename}.csv"
    job_config = bigquery.QueryJobConfig(
      default_dataset=dataset_id,
      use_query_cache=True,
      destination=tmp_table,
      write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
    query_job = bq_client.query(sql, job_config=job_config)
    step1 = query_job.result()
    total_rows = step1.total_rows
    extract_config = bigquery.ExtractJobConfig(
      field_delimiter=',',
      print_header=True,
      destination_format='CSV'
    )
    extract_job = bq_client.extract_table(source=tmp_table, destination_uris=destination_uri, job_config=extract_config)
    step2 = extract_job.result()
    ans ={
      'status': step2.state,
      'total_rows': total_rows
    }
    if step2.errors:
      ans['error'] = step2.errors
    return ans
  except BadRequest as e:
    return {'error': e.errors}
  except Exception as e:
    return {'error': e}
  