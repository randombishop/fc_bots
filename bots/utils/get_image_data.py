import requests


def get_image_data(url):
  try:
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    # For imgur links, modify the URL to get the direct image
    if 'imgur.com' in url and not url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
      url = url.replace('imgur.com', 'i.imgur.com')
      if not url.endswith('.jpg'):
        url += '.jpg'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content_type = response.headers.get('content-type', '')
    if not any(mime in content_type.lower() for mime in ['gif', 'png', 'jpeg', 'jpg']):
      raise ValueError(f"Unsupported image type: {content_type}")
    image_data = response.content
    import base64
    encoded = base64.b64encode(image_data).decode('utf-8')
    return f"data:{content_type};base64,{encoded}"
  except Exception as e:
    print(f"Error getting image data from {url}: {str(e)}")
    return None