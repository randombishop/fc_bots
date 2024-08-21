import os
import pandas
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest


project_id = os.environ['GCP_PROJECT_ID']
dataset_id = project_id + '.' + os.environ['GCP_DATASET_ID']
dataset_tmp = project_id + '.' + os.environ['GCP_DATASET_TMP']
bq_client = bigquery.Client(project=project_id)
debug = False


def dry_run(sql, params=[]):
  if debug:
    print("---- big query dry run start ----")
    print(f"SQL: {sql}")
    print(f"Params: {params}")
  job_config = bigquery.QueryJobConfig(
    query_parameters=params,
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
  if debug:
    print(f"Dry run result: {ans}")
    print("---- big query dry run end ----")
  return ans
  

def execute(sql, params=[]):
  if debug:
    print("---- big query execute start ----")
    print(f"SQL: {sql}")
    print(f"Params: {params}")
  job_config = bigquery.QueryJobConfig(
    query_parameters=params,
    default_dataset=dataset_id, 
    use_query_cache=True)
  query_job = bq_client.query(sql, job_config)
  response = query_job.result()
  if debug:
    print(f"Num results: {response.total_rows}")
    print("---- big query execute end ----")
  return response
  

def sql_to_gcs(sql, folder, filename, params=[]):
  if debug:
    print("---- big query sql_to_gcs start ----")
    print(f"SQL: {sql}")
    print(f"Params: {params}")
  tmp_table = f"{dataset_tmp}.{filename}"
  bucket_name = os.environ['GCP_BOT_BUCKET_TMP']
  destination_uri = f"gs://{bucket_name}/{folder}/{filename}.csv"
  job_config = bigquery.QueryJobConfig(
    query_parameters=params,
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
  if debug:
    print(f"Result: {ans}")
    print("---- big query sql_to_gcs end ----")
  return ans
  

def to_array(result):
  values = [x.values() for x in result]
  columns = list(result[0].keys())
  return {'values': values, 'columns': columns}