import requests
import os
from bots.utils.format_when import format_when


def get_user_info_by_fids(fids):
  fids = ','.join([str(fid) for fid in fids])
  url = f'https://api.neynar.com/v2/farcaster/user/bulk?fids={fids}'
  response = requests.get(url, headers={
    'x-api-key': os.getenv('NEYNAR_API_KEY')
  })
  response.raise_for_status() 
  infos = response.json()
  return [parse_user_info(info) for info in infos['users']]


def get_user_info_by_fid(fid):
  infos = get_user_info_by_fids([fid])
  if infos is not None and len(infos) > 0:
    return infos[0]
  return None


def get_user_info_by_name(name):
  url = f'https://api.neynar.com/v2/farcaster/user/by_username?username={name}'
  response = requests.get(url, headers={
    'x-api-key': os.getenv('NEYNAR_API_KEY')
  })
  response.raise_for_status()
  info = response.json()
  return parse_user_info(info['user'])


def parse_user_info(user):
  if user is None:
    return None
  parsed = {
    'fid': int(user['fid']),
    'user_name': user['username'],
    'display_name': user['display_name'],
    'pfp': user['pfp_url'],
    'bio': user['profile']['bio']['text'],
    'custody_address': user['verified_addresses']['eth_addresses'][0],
    'num_following': int(user['following_count']),
    'num_followers': int(user['follower_count'])
  }
  return parsed


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
  url = f'https://api.neynar.com/v2/farcaster/cast?identifier={hash}&type=hash'
  response = requests.get(url, headers={
    'x-api-key': os.getenv('NEYNAR_API_KEY')
  })
  response.raise_for_status()
  info = response.json()
  return parse_cast(info['cast'])


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
    'when': format_when(cast_info['timestamp'])
  }
  if 'embeds' in cast_info and len(cast_info['embeds']) > 0:
      embed = cast_info['embeds'][0]
      if 'url' in embed:
        cast['quote'] = {'url': embed['url']}
      elif 'cast' in embed:
        cast['quote'] = {'text': embed['cast']['text'], 'fid': int(embed['cast']['author']['fid']), 'username': embed['cast']['author']['username']}
  return cast