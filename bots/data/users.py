from dotenv import load_dotenv
load_dotenv()
import sys
import time
from bots.data.wield import get_user_info_by_fid, get_user_info_by_name


def get_username(fid):
  user_info = get_user_info_by_fid(fid)
  if user_info is not None:
    return user_info['user_name']
  else:
    return None


def get_fid(username):
  user_info = get_user_info_by_name(username)
  if user_info is not None:
    return user_info['fid']
  else:
    return None



if __name__ == "__main__":
  input = input("Enter user FID or username: ")
  try:
    fid = int(input)
    print(fid, 'fid->username', get_username(fid))
  except:
    username = input.lower()
    print(username, 'username->fid', get_fid(username)) 
