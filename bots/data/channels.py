from bots.data.dsart import fetch_channels


_channels = fetch_channels()
_channels_by_id = {x['id'].lower(): x['url'] for x in _channels}
_channels_by_name = {x['name'].lower(): x['url'] for x in _channels}
_channels_by_url = {x['url']: x['id'] for x in _channels}

def get_channels():
  return _channels


def get_channels_map():
  return _channels_by_id, _channels_by_name


def get_channel_by_url(url):
  return _channels_by_url[url] if url in _channels_by_url else None


def get_channel_url(channel):
  if channel is None or channel in ['', 'None']:
    return None
  if channel in _channels_by_id:
    return _channels_by_id[channel]
  elif channel in _channels_by_name:
    return _channels_by_name[channel]
  elif channel.startswith('http://') or channel.startswith('https://'):
    return channel
  else:
    return None