from dotenv import load_dotenv
load_dotenv()
import os
import sys
import requests
from datetime import datetime


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


def get_user_info_by_fid(fid):
  url = 'https://build.wield.xyz/farcaster/v2/user'
  response = requests.get(url, params={'fid': fid}, headers={
    'API-KEY': os.getenv('FARQUEST_API_KEY'),
    'Accept': 'application/json'
  })
  response.raise_for_status()  # Raise an error for bad responses
  user = response.json()['result']['user']
  return parse_user_info(user)
  

def get_user_info_by_name(name):
  url = 'https://build.wield.xyz/farcaster/v2/user-by-username'
  response = requests.get(url, params={'username': name}, headers={
    'API-KEY': os.getenv('FARQUEST_API_KEY'),
    'Accept': 'application/json'
  })
  response.raise_for_status()  # Raise an error for bad responses
  user = response.json()['result']['user']
  return parse_user_info(user)
  

def get_user_info(user):
  try:
    fid = int(user)
    return get_user_info_by_fid(fid)
  except ValueError:
    return get_user_info_by_name(user)


def get_cast_info(hash):
  url = 'https://build.wield.xyz/farcaster/v2/cast'
  response = requests.get(url, params={'hash': hash}, headers={
    'API-KEY': os.getenv('FARQUEST_API_KEY'),
    'Accept': 'application/json'
  })  
  response.raise_for_status()  # Raise an error for bad responses
  cast = response.json()['result']['cast']
  return cast


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
