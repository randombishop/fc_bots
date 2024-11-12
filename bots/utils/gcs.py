from google.cloud import storage
import os


def upload_to_gcs(local_file, target_folder, target_file):
  if 'GCP_BOT_BUCKET' in os.environ:
    bucket_name = os.environ['GCP_BOT_BUCKET']
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    destination_blob_name = os.path.join(target_folder, target_file)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file)
    print(f"File {local_file} uploaded to {destination_blob_name} in bucket {bucket_name}.")
  else:
    print('Warning: GCP_BOT_BUCKET is not set, skipping upload to GCS.')

