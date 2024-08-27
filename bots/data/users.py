from dotenv import load_dotenv
load_dotenv()
import sys
import time
from bots.data.pg import pg_connection


def get_username(fid):
  sql = """
  select body->>'value' as user_name
  from messages
  where fid={}
  and type = 11 
  and body->>'type' = '6'
  order by timestamp desc
  limit 1
  """
  with pg_connection.cursor() as cursor:
    cursor.execute(sql.format(fid))
    username = cursor.fetchone()
  if username is not None:
    return username[0]
  else:
    return None


def get_fid(username):
  sql = """
  select fid
  from messages
  where body->>'value'='{}'
  and type = 11 
  and body->>'type' = '6'
  order by timestamp desc
  limit 1;
  """
  with pg_connection.cursor() as cursor:
    cursor.execute(sql.format(username))
    fid = cursor.fetchone()
  if fid is not None:
    return fid[0]
  else:
    return None


def get_usernames(fids):
  sql = """
  select fid, body->>'value' as user
  from messages
  where fid in ({})
  and type = 11 
  and body->>'type' = '6'
  order by timestamp desc
  limit 1
  """
  with pg_connection.cursor() as cursor:
    cursor.execute(sql.format(",".join([str(fid) for fid in fids])))
    ans = cursor.fetchall()
  return {int(row[0]): row[1] for row in ans}


if __name__ == "__main__":
  t0 = time.time()
  input = sys.argv[1]
  try:
    fid = int(input)
    print(fid, 'fid->username', get_username(fid))
  except:
    username = input.lower()
    print(username, 'username->fid', get_fid(username))
  print('time:', time.time() - t0)
  
