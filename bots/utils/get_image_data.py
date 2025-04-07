import requests
import base64


def get_image_data(url):
  try:
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    # For imgur links, modify the URL to get the direct image
    if 'imgur.com' in url and not url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
      url = url.replace('imgur.com', 'i.imgur.com')
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content_type = response.headers.get('content-type', '')
    if not content_type in ['gif', 'png', 'jpeg', 'jpg']:
      print(f"WARNING: Unsupported image type from {url}: {content_type}")
      return None
    image_data = response.content
    encoded = base64.b64encode(image_data).decode('utf-8')
    return f"data:{content_type};base64,{encoded}"
  except Exception as e:
    print(f"WARNING: Could not get image data from {url}: {str(e)}")
    return None