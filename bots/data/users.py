import json
from bots.data.wield import get_user_info_by_fid, get_user_info_by_name
from bots.data.dune import run_query
from dune_client.types import QueryParameter
from datetime import datetime, timedelta


def get_username(fid):
  if fid is None:
    raise Exception("get_username: must provide fid")
  user_info = get_user_info_by_fid(fid)
  if user_info is not None:
    return user_info['user_name']
  else:
    return None


def get_fid(username):
  if username is None:
    raise Exception("get_fid: must provide username")
  user_info = get_user_info_by_name(username)
  if user_info is not None:
    return user_info['fid']
  else:
    return None


def get_words_dict(fid):
  query_id = 4257892
  params = [QueryParameter.number_type(name="fid", value=fid)]
  response = run_query(query_id, params)
  rows = response.to_dict('records')
  if len(rows) == 0:
    return None
  else:
    s = rows[0]['keywords']
    if s is None:
      return None
    else:
      return json.loads(s)


def get_favorite_users(fid):
  query_id = 4258114
  params = [
    QueryParameter.number_type(name="fid", value=fid),
    QueryParameter.number_type(name="limit", value=10)
  ]
  return run_query(query_id, params)


def get_top_daily_casters(channel, limit=10):
  query_id = 4258259
  params = [
    QueryParameter.text_type(name="parent_url", value=channel if channel is not None else '*'),
    QueryParameter.number_type(name="limit", value=limit)
  ]
  df = run_query(query_id, params)
  today = datetime.today()
  deltas = list(range(1,11))
  days = [(today - timedelta(days=x)).strftime("%Y-%m-%d") for x in deltas]
  rename = {f"d-{deltas[i]}": days[i] for i in range(len(deltas))}
  rename['user_name']='User'
  df.rename(columns=rename, inplace=True)
  return df


if __name__ == "__main__":
  input = input("Enter user FID or username: ")
  try:
    fid = int(input)
    print(fid, 'fid->username', get_username(fid))
  except:
    username = input.lower()
    print(username, 'username->fid', get_fid(username)) 
