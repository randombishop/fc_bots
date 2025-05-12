import requests
import os
from bots.utils.format_when import format_when


API_URL = 'https://api.neynar.com/v2/farcaster/'


def call_neynar_api(endpoint, params):
  response = requests.get(API_URL + endpoint, headers={
    'x-api-key': os.getenv('NEYNAR_API_KEY')
  }, params=params)
  response.raise_for_status()
  return response.json()


def get_user_info_by_fids(fids):
  fids = ','.join([str(fid) for fid in fids])
  url = 'user/bulk'
  infos = call_neynar_api(url, {'fids': fids})
  return [parse_user_info(info) for info in infos['users']]


def get_user_info_by_fid(fid):
  infos = get_user_info_by_fids([fid])
  if infos is not None and len(infos) > 0:
    return infos[0]
  return None


def get_user_info_by_name(name):
  url = 'user/by_username'
  info = call_neynar_api(url, {'username': name})
  return parse_user_info(info['user'])


def is_fid(user):
  try:
    return int(user)
  except ValueError:
    return None
  

def get_user_info(user):
  fid = is_fid(user)
  if fid is not None:
    return get_user_info_by_fid(fid)
  else:
    return get_user_info_by_name(user)
  


def get_cast_info(hash):
  url = 'cast'
  params = {
    'identifier': hash,
    'type': 'hash'
  }
  info = call_neynar_api(url, params)
  return parse_cast(info['cast'])


def get_casts_ids(hashes):
  url = 'casts'
  params = {
    'casts': ','.join(hashes)
  }
  info = call_neynar_api(url, params)
  array = [parse_cast(x) for x in info['result']['casts']]
  return {x['hash']: x for x in array}


def get_casts_user(fid, limit=25):
  url = 'feed/user/casts'
  params = {
    'fid': fid,
    'include_replies': 'false',
    'limit': limit
  }
  info = call_neynar_api(url, params)
  return [parse_cast(x) for x in info['casts']]


def get_casts_channel(channel_url, limit=25):
  url = 'feed/parent_urls'
  params = {
    'with_recasts': 'true',
    'limit': limit,
    'parent_urls': channel_url
  }
  info = call_neynar_api(url, params)
  return [parse_cast(x) for x in info['casts']]


def get_casts_user_channel(fid, channel_url, limit=25):
  url = 'feed/user/casts'
  params = {
    'fid': fid,
    'include_replies': 'false',
    'parent_urls': channel_url,
    'limit': limit
  }
  info = call_neynar_api(url, params)
  return [parse_cast(x) for x in info['casts']]


def search_casts(query, mode, limit=25):
  url = 'cast/search'
  params = {
    'q': query,
    'mode': mode,
    'limit': limit,
    'sort_type': 'algorithmic'
  }
  info = call_neynar_api(url, params)
  return [parse_cast(x) for x in info['result']['casts']]


def get_user_likes(fid, limit=25):
  url = 'reactions/user'
  params = {
    'fid': fid,
    'limit': limit,
    'type': 'likes'
  }
  info = call_neynar_api(url, params)
  return [parse_like(x) for x in info['reactions']]


def get_user_replies_and_recasts(fid, limit=25):
  url = 'feed/user/replies_and_recasts'
  params = {
    'fid': fid,
    'limit': limit,
    'filter': 'all'
  }
  info = call_neynar_api(url, params)
  ans = [parse_replies_recasts(fid, x) for x in info['casts']]
  parent_hashes = [x['cast']['parent_hash'] for x in ans if x['cast']['parent_hash'] is not None]
  if len(parent_hashes) > 0:
    parent_casts = get_casts_ids(parent_hashes)
    for x in ans:
      if x['cast']['parent_hash'] is not None and x['cast']['parent_hash'] in parent_casts:
        x['cast']['parent_cast'] = parent_casts[x['cast']['parent_hash']]
  return ans





################################################################################
### Parse API responses into compact data structures
################################################################################
def parse_custody_address(user):
  try: 
    return user['verified_addresses']['eth_addresses'][0]
  except:
    return None


def parse_user_info(user):
  if user is None:
    return None
  parsed = {
    'fid': int(user['fid']),
    'user_name': user['username'],
    'display_name': user['display_name'],
    'pfp': user['pfp_url'],
    'bio': user['profile']['bio']['text'],
    'custody_address': parse_custody_address(user),
    'num_following': int(user['following_count']),
    'num_followers': int(user['follower_count'])
  }
  return parsed


def parse_cast(cast_info):
  if cast_info is None:
    return None
  cast = {
    'hash': cast_info['hash'],
    'fid': int(cast_info['author']['fid']),
    'username': cast_info['author']['username'],
    'text': cast_info['text'],
    'mentions': [x['fid'] for x in cast_info['mentioned_profiles']] if 'mentioned_profiles' in cast_info else [], 
    'mentionsPos': [x['start'] for x in cast_info['mentioned_profiles_ranges']] if 'mentioned_profiles_ranges' in cast_info else [],
    'parent_fid': cast_info['parent_author']['fid'] if 'parent_author' in cast_info else None,
    'parent_hash': cast_info['parent_hash'] if 'parent_hash' in cast_info else None,
    'timestamp': cast_info['timestamp'],
    'when': format_when(cast_info['timestamp']),
    'num_likes': int(cast_info['reactions']['likes_count']) if 'reactions' in cast_info and 'likes_count' in cast_info['reactions'] else 0,
    'num_recasts': int(cast_info['reactions']['recasts_count']) if 'reactions' in cast_info and 'recasts_count' in cast_info['reactions'] else 0,
    'num_replies': int(cast_info['replies']['count']) if 'replies' in cast_info and 'count' in cast_info['replies'] else 0
  }
  if 'embeds' in cast_info and len(cast_info['embeds']) > 0:
      embed = cast_info['embeds'][0]
      if 'url' in embed:
        cast['quote'] = {'url': embed['url']}
      elif 'cast' in embed:
        cast['quote'] = {'text': embed['cast']['text'], 'fid': int(embed['cast']['author']['fid']), 'username': embed['cast']['author']['username']}
  return cast


def parse_like(like):
  cast = parse_cast(like['cast'])
  return {
    'type': 'like',
    'timestamp': like['reaction_timestamp'],
    'when': format_when(like['reaction_timestamp']),
    'cast': cast
  }


def parse_replies_recasts(fid, info):
  cast = parse_cast(info)
  reaction = None
  if cast['fid'] == fid and cast['parent_fid'] is not None: 
    reaction = 'reply'
  else:
    reaction = 'recast'
  return {
    'type': reaction,
    'timestamp': info['timestamp'],
    'when': format_when(info['timestamp']),
    'cast': cast
  }
