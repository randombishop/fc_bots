import requests


def get_url_data(url):
  data = None
  mime_type = None
  try:  
    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.content
    mime_type = response.headers['Content-Type']
  except Exception as e:
    print(f'Error fetching data from {url}: {e}')
  if data is None or mime_type is None:
    print(f'Could not obtain data and mime type from {url}')
  return data, mime_type