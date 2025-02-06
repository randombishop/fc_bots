from bots.data.channels import get_channels_map
from bots.data.users import get_fid, get_username


def is_fid(value):
  if value is None:
    return False
  else:
    try:
      int_value = int(value)
      return int_value > 0 and int_value<10000000
    except:
      return False


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
    if s in ['null', 'undefined', 'none', 'me', 'you', 'myself', 'self', 'user', 'unknown_user', '', '*']:
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
    if s in ['null', 'undefined', 'none', 'channel', '<channel>', 'here', 'this']:
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


def read_string(params, key, default=None, max_length=256):
  ans = default
  if key in params and params[key] is not None:
    ans = str(params[key])
    if len(ans) > max_length:
      ans = ans[:max_length]
    if ans.lower() in ['null', 'undefined', 'none']:
      ans = None
  return ans


def read_boolean(params, key):
  if key in params and params[key] is not None:
    return is_true(params[key])
  else:
    return False


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


def read_channel(params, current_channel=None, default_to_current=False):
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
    else:
      channel = None  
  if channel is None and default_to_current:
    channel = current_channel
  return channel


def read_user(params, fid_origin=None, default_to_origin=False):
  fid = None
  user_name = None
  if 'user' in params and is_specific_user(params['user']):
    s = str(params['user']).lower()
    if s.startswith('@'):
      s = s[1:]
    if s.startswith('fid#'):
      s = s[4:]
    if is_fid(s):
      fid = int(s)
      user_name = get_username(fid)
    else:
      try:
        user_name = s
        fid = get_fid(user_name)
      except:
        user_name = None
        fid = None
  if fid is None and fid_origin is not None and default_to_origin:
    fid = fid_origin
    user_name = get_username(fid)
  return fid, user_name
  
