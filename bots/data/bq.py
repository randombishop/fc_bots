import os
from google.cloud import bigquery


project_id = os.environ['GCP_PROJECT_ID']
dataset_id = project_id + '.' + os.environ['GCP_DATASET_ID']
bq_client = bigquery.Client(project=project_id)
