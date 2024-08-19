from bots.data.channels import get_channels


def read_channel(params):
  channel = None
  if ('channel' in params) and (params['channel'] is not None) and (params['channel'] != 'null') and (len(params['channel']) > 0):
    channels_by_id, channels_by_name = get_channels()
    channel = params['channel']
    channel_lower_case = channel.lower()
    if channel_lower_case in channels_by_id:
      channel = channels_by_id[channel_lower_case]
    elif channel_lower_case in channels_by_name:
      channel = channels_by_name[channel_lower_case]
  return channel

def read_int(params, key, default, min, max):
  ans = default
  try:
    if key in params:
      ans = int(params[key])
      ans = max(ans, min)
      ans = min(ans, max)
  except:
    pass
  return ans

def read_keywords(params):
  keywords = []
  if 'keywords' in params and params['keywords'] is not None and len(params['keywords']) > 0:
    keywords_string = params['keywords']
    keywords_string = keywords_string.replace(' ', ',')
    keywords_string = keywords_string.replace('\n', ',')
    keywords_string = keywords_string.lower()
    keywords = keywords_string.split(',')
  return keywords