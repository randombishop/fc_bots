from dotenv import load_dotenv
load_dotenv()
import os
import sys
import requests
import time
from datetime import datetime


last_call = 0
min_delay = 5
def cooldown():
  global last_call
  now = time.time()
  elapsed = now - last_call
  if elapsed < min_delay:
    time.sleep(min_delay - elapsed) 
  last_call = time.time()


def get_user_info_by_fid(fid):
  cooldown()
  url = 'https://build.wield.xyz/farcaster/v2/user'
  response = requests.get(url, params={'fid': fid}, headers={
    'API-KEY': os.getenv('FARQUEST_API_KEY'),
    'Accept': 'application/json'
  })
  response.raise_for_status()  # Raise an error for bad responses
  user = response.json()['result']['user']
  return parse_user_info(user)
  

def get_user_info_by_name(name):
  cooldown()
  url = 'https://build.wield.xyz/farcaster/v2/user-by-username'
  response = requests.get(url, params={'username': name}, headers={
    'API-KEY': os.getenv('FARQUEST_API_KEY'),
    'Accept': 'application/json'
  })
  response.raise_for_status()  # Raise an error for bad responses
  user = response.json()['result']['user']
  return parse_user_info(user)
  

def get_cast_info(hash):
  cooldown()
  url = 'https://build.wield.xyz/farcaster/v2/cast'
  response = requests.get(url, params={'hash': hash}, headers={
    'API-KEY': os.getenv('FARQUEST_API_KEY'),
    'Accept': 'application/json'
  })  
  response.raise_for_status()  # Raise an error for bad responses
  cast = response.json()['result']['cast']
  return cast


def get_user_info(user):
  try:
    fid = int(user)
    return get_user_info_by_fid(fid)
  except ValueError:
    return get_user_info_by_name(user)


def parse_user_info(user):
  return {
    'fid': int(user['fid']),
    'user_name': user['username'],
    'display_name': user['displayName'],
    'pfp': user['pfp'],
    'bio': user['bio'],
    'fid_registered_at': datetime.fromtimestamp(user['registeredAt'] / 1000),
    'custody_address': user['custodyAddress'],
    'connected_address': user['connectedAddress']
  }



if __name__ == '__main__':
  if sys.argv[1]=='user':
    user_input = input("Enter user FID or username: ")
    user_info = get_user_info(user_input)
    print(user_info)
  elif sys.argv[1]=='cast':
    hash = sys.argv[2]
    print('Fetching cast', hash)
    cast = get_cast_info(hash)
    print(cast)
