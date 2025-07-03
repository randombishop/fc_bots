import requests


def fetch_channels():
  response = requests.get('https://fc.datascience.art/channels/list', verify=False)
  if response.status_code == 200:
    return response.json()
  return []