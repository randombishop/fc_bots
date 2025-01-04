from bots.data.dsart import fetch_channels


_channels = fetch_channels()
_channels_by_id = {x['id'].lower(): x['url'] for x in _channels}
_channels_by_name = {x['name'].lower(): x['url'] for x in _channels}


def get_channels():
  return _channels


def get_channels_map():
  return _channels_by_id, _channels_by_name

