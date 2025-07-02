import requests
import os
import time


API_KEY = os.getenv("SKYVERN_API_KEY")
USERNAME = os.getenv("SKYVERN_USERNAME")
PASSWORD = os.getenv("SKYVERN_PASSWORD")
URL_WORKFLOWS = os.getenv("SKYVERN_WORKFLOW_URL")
TIMEOUT = 300


def start_workflow(workflow_id, payload_data):
  url = f"{URL_WORKFLOWS}/{workflow_id}/run"
  headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
  }
  payload = {
    "data": payload_data,
    "proxy_location": "RESIDENTIAL"
  }
  response = requests.post(
    url,
    headers=headers,
    json=payload,
    auth=(USERNAME, PASSWORD)
  )
  status = response.status_code
  if status != 200:
    raise Exception(f"Skyvern API returned status code {status}")
  result = response.json()
  if 'workflow_run_id' not in result:
    raise Exception(f"Skyvern API returned invalid response: {result}")
  return result['workflow_run_id']


def check_workflow(workflow_id, run_id):
  url = f"{URL_WORKFLOWS}/{workflow_id}/runs/{run_id}"
  headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
  }
  response = requests.get(url, headers=headers, auth=(USERNAME, PASSWORD))
  status = response.status_code
  if status != 200:
    raise Exception(f"Skyvern API returned status code {status}")
  result = response.json()
  return result


def get_workflow_result(workflow_id, run_id):
  start_time = time.time()
  while True:
    result = check_workflow(workflow_id, run_id)
    print(f"Waiting for skyvern worflow {workflow_id}/{run_id} to complete... Status: {result['status']}")
    if result['status'] not in ['running', 'created']:
      return result
    if time.time() - start_time > TIMEOUT:
      raise Exception(f"Workflow timed out after {TIMEOUT} seconds")
    time.sleep(10)