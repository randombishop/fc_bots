from bots.data.channels import get_channels_map
from bots.data.users import get_fid, get_username


def is_true(value):
  if value==True:
    return True
  else:
    return str(value).lower() in ['true', 'yes', '1']


def is_specific_user(value):
  if value is None:
    return False
  else:
    s = str(value).lower()
    if s.startswith('@'):
      s = s[1:]
    if 'username' in s:
      return False
    if s in ['null', 'undefined', 'none', 'me', 'you', 'myself', 'self', 'user']:
      return False
    if len(s) == 0:
      return False
  return True

def is_specific_channel(value):
  if value is None:
    return False
  else:
    s = str(value).lower()
    if s.startswith('/'):
      s = s[1:]
    if s in ['null', 'undefined', 'none', 'channel', '<channel>']:
      return False
    if len(s) == 0:
      return False
  return True

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
    if ans.lower() in ['null', 'undefined', 'none']:
      ans = None
  return ans


def read_channel(params):
  channel = None
  if ('channel' in params) and is_specific_channel(params['channel']):
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
    if keyword_string in ['null', 'undefined', 'none']:
      return None
    elif len(keyword_string) > 3:
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

def read_fid(params, fid_origin=None):
  if 'user' in params and is_specific_user(params['user']):
    s = str(params['user']).lower()
    if s.startswith('@'):
      s = s[1:]
    try:
      fid = int(s)
      return fid
    except:
      return get_fid(s)
  return fid_origin

def read_username(params, fid_origin=None):
  if 'user' in params and is_specific_user(params['user']):
    s = str(params['user']).lower()
    if s.startswith('@'):
      s = s[1:]
    try:
      fid = int(s)
      return get_username(fid)
    except:
      return s
  if fid_origin is not None:
    return get_username(fid_origin)
  return None
