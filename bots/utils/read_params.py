from bots.data.channels import get_channels_map
from bots.data.users import get_fid, get_username


def read_int(params, key, default, min, max):
  ans = default
  try:
    if key in params and params[key] is not None:
      ans = int(params[key])
      ans = max(ans, min)
      ans = min(ans, max)
  except:
    pass
  return ans


def read_string(params, key, default, max_length):
  ans = default
  if key in params and params[key] is not None:
    ans = str(params[key])
    if len(ans) > max_length:
      ans = ans[:max_length]
  return ans


def read_channel(params):
  channel = None
  if ('channel' in params) and (params['channel'] is not None) and (params['channel'] != 'null') and (len(params['channel']) > 0):
    channels_by_id, channels_by_name = get_channels_map()
    channel = params['channel']
    channel_lower_case = channel.lower()
    if channel_lower_case.startswith('/'):
      channel_lower_case = channel_lower_case[1:]
    if channel_lower_case in channels_by_id:
      channel = channels_by_id[channel_lower_case]
    elif channel_lower_case in channels_by_name:
      channel = channels_by_name[channel_lower_case]
  return channel


def read_keyword(params):
  if 'keyword' in params and params['keyword'] is not None:
    keyword_string = str(params['keyword'])
    keyword_string = keyword_string.lower()
    keyword_string = keyword_string.strip()
    if len(keyword_string) > 3:
      return keyword_string
    else:
      return None

def read_category(params):
  if 'category' in params and params['category'] is not None:
    category = params['category'].lower()
    if not category.startswith('c_'):
      category = 'c_' + category
    if category not in ['c_arts', 'c_business', 'c_crypto', 'c_culture', 'c_money', 'c_nature', 'c_politics', 'c_sports', 'c_tech_science']:
      return None
    else:
      return category
  return None

def read_fid(params):
  if 'user' in params and params['user'] is not None:
    try:
      fid = int(params['user'])
      return fid
    except:
      username = params['user'].lower()
      if username.startswith('@'):
        username = username[1:]
      return get_fid(username)
  return None

def read_username(params):
  if 'user' in params and params['user'] is not None:
    try:
      fid = int(params['user'])
      return get_username(fid)
    except:
      username = params['user'].lower()
      if username.startswith('@'):
        username = username[1:]
      return username
  return None