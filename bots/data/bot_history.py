from bots.data.users import get_top_daily_casters, get_user_profiles
from bots.data.pg import engine, metadata, get_session
from sqlalchemy import text, Table
import random


bot_cast_table = Table('bot_cast', metadata, autoload_with=engine, schema='app')


def save_bot_cast(bot_cast):
  with get_session() as session:
    stmt = bot_cast_table.insert().values(bot_cast)
    session.execute(stmt)
    

def get_bot_casts(bot_id, action_channel='*', limit=50, days=60):
  with get_session() as session:
    sql = text("""
    SELECT action_channel, casted_text, casted_embeds, casted_at,
           EXTRACT(EPOCH FROM (NOW() - casted_at)) / 3600 hours
    FROM app.bot_cast
    WHERE bot_id = :bot_id
    AND casted_at >= NOW() - INTERVAL ':days days'
    AND cast_hash = root_hash
    AND casted_text is not NULL    
    AND (:action_channel='*' or action_channel=:action_channel)
    ORDER BY casted_at DESC
    LIMIT :limit
    """)
    result = session.execute(sql, {'bot_id': bot_id, 
                                   'days': days,
                                   'limit': limit, 
                                   'action_channel': action_channel})
    return result.mappings().all()
  

def get_bot_prompts_stats(bot_id):
  with get_session() as session:
    sql = text("""
    WITH t0 AS (
    SELECT 
      action_id,
      action_channel,
      max(casted_at) as last_cast,
      EXTRACT(EPOCH FROM (NOW() - MAX(casted_at))) / 3600 hours_ago           
      FROM app.bot_cast
      WHERE casted_at >= NOW() - INTERVAL '60 days' 
      AND bot_id=:bot_id
      AND cast_hash = root_hash
      AND action_id is not NULL
    AND action_channel is not NULL
      GROUP by action_id, action_channel
      ),
    t1 AS (
      SELECT action_id, action_channel,
          count(*) num_posts,
          avg(num_replies) avg_replies, 
          avg(num_likes) avg_likes,
          avg(num_recasts) avg_recasts
      FROM app.bot_cast
      WHERE bot_id = :bot_id
      AND num_likes is not NULL
      AND casted_at >= NOW() - INTERVAL '60 days'
      AND action_id is not NULL
      AND action_channel is not NULL
      GROUP BY action_id, action_channel
    ),
    t2 AS (
      SELECT t0.action_id, t0.action_channel, SUM(channel_counts.num_casts) as channel_activity
      FROM t0 LEFT JOIN ds.channel_counts on t0.action_channel=channel_counts.channel
      WHERE channel_counts.counted_at > t0.last_cast
      GROUP BY t0.action_id, t0.action_channel
    )        
    SELECT 
      t0.action_channel as channel,
      t0.action_id as id, 
      t0.last_cast,
      t0.hours_ago,
      t1.num_posts as bot_activity, 
      t1.avg_replies, t1.avg_likes, t1.avg_recasts,
      t2.channel_activity
    FROM t0 FULL OUTER JOIN t1 ON t0.action_id = t1.action_id AND t0.action_channel = t1.action_channel
    LEFT JOIN t2 ON t0.action_id = t2.action_id AND t0.action_channel = t2.action_channel;
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    return result.mappings().all()
  
        
def get_random_user(bot_id):
  with get_session() as session:
    sql = text("""
    WITH candidates as (
      SELECT DISTINCT username FROM ds.trending_casts WHERE timestamp >= NOW() - INTERVAL '5 days'
    ),
    exclude_users as (
      SELECT DISTINCT user_name as u FROM ds.user_profile
    )
    SELECT username FROM candidates WHERE username not in (SELECT u FROM exclude_users) ORDER BY random() LIMIT 1
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    row = result.mappings().fetchone()
    if row is not None:
      return row['username']
    else:
      return None
    

def get_random_user_in_channel(bot_id, channel_url):
  df_top_users = get_top_daily_casters(channel_url, limit=20)
  df_top_users = df_top_users[df_top_users['fid'] != bot_id]
  top_users = df_top_users['User'].tolist()
  if len(top_users) == 0:
    return None
  saved_profiles = get_user_profiles(bot_id)
  saved_profiles = {row['user_name']: row['fid'] for row in saved_profiles}
  candidates = [user for user in top_users if user not in saved_profiles]
  if len(candidates) == 0:
    return None
  return random.choice(candidates)
