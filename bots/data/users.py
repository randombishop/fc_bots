import json
from sqlalchemy import Table, select
from bots.data.pg import engine, metadata, get_session
from bots.data.neynar import get_user_info_by_fid, get_user_info_by_name
from bots.data.dune import run_query
from dune_client.types import QueryParameter
from datetime import datetime, timedelta


user_profile_table = Table('user_profile', metadata, autoload_with=engine, schema='ds')
user_profile_embed_table = Table('user_profile_embed', metadata, autoload_with=engine, schema='ds')


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
    return None
  user_info = get_user_info_by_name(username)
  if user_info is not None:
    return user_info['fid']
  else:
    return None


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


def get_user_profile(bot_id, fid):
  with get_session() as session:
    stmt = user_profile_table.select().where(user_profile_table.c.bot_id == bot_id).where(user_profile_table.c.fid == fid)
    result = session.execute(stmt).mappings().fetchone()
    return result
  
def get_user_profiles(bot_id):
  with get_session() as session:
    stmt = select(user_profile_table.c.fid, user_profile_table.c.user_name).where(user_profile_table.c.bot_id == bot_id)
    result = session.execute(stmt).mappings().fetchall()
    return result
  
def get_user_profile_embed(bot_id, fid, part):
  with get_session() as session:
    stmt = (user_profile_embed_table
              .select()
              .where(user_profile_embed_table.c.bot_id == bot_id)
              .where(user_profile_embed_table.c.fid == fid)
              .where(user_profile_embed_table.c.part == part))
    result = session.execute(stmt).mappings().fetchone()
    return result

def save_user_profile(profile):
  if get_user_profile(profile['bot_id'], profile['fid']) is None:
    with get_session() as session:
      session.execute(user_profile_table.insert().values(**profile))
    print('Inserted new user profile in pg')
  else:
    with get_session() as session:
      session.execute(user_profile_table
                      .update()
                      .where(user_profile_table.c.bot_id == profile['bot_id'])
                      .where(user_profile_table.c.fid == profile['fid'])
                      .values(**profile))
    print('Updated existing user profile in pg')

def save_user_profile_embed(bot_id, fid, part, embed):
  if get_user_profile_embed(bot_id, fid, part) is None:
    with get_session() as session:
      session.execute(user_profile_embed_table
                      .insert()
                      .values(bot_id=bot_id, fid=fid, part=part, embed=embed))
    print('Inserted new embedding in pg')
  else:
    with get_session() as session:
      session.execute(user_profile_embed_table
                      .update()
                      .where(user_profile_embed_table.c.bot_id == bot_id)
                      .where(user_profile_embed_table.c.fid == fid)
                      .where(user_profile_embed_table.c.part == part)
                      .values(embed=embed))
    print('Updated existing embedding in pg')
    
def save_user_profile_embeds(profile):
  parts = ['bio', 'pfp', 'casts', 'engagement', 'avatar']
  for part in parts:
    if profile[f'{part}_embed'] is not None:
      save_user_profile_embed(profile['bot_id'], profile['fid'], part, profile[f'{part}_embed'])
