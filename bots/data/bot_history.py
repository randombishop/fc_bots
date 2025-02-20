from bots.data.users import get_top_daily_casters
from bots.data.pg import get_session
from sqlalchemy import text
import random


def get_bot_casts(bot_id, action_channel='*', no_channel=False, selected_action='*', limit=50, days=60):
  with get_session() as session:
    sql = text("""
    SELECT selected_action, action_prompt, action_channel, casted_text, casted_embeds, casted_at,
           EXTRACT(EPOCH FROM (NOW() - casted_at)) / 3600 hours
    FROM app.bot_cast
    WHERE bot_id = :bot_id
    AND casted_at >= NOW() - INTERVAL ':days days'
    AND cast_hash = root_hash
    AND casted_text is not NULL    
    AND (:action_channel='*' or action_channel=:action_channel)
    AND (:no_channel=FALSE or action_channel is NULL)
    AND (:selected_action='*' or selected_action=:selected_action)            
    ORDER BY casted_at DESC
    LIMIT :limit
    """)
    result = session.execute(sql, {'bot_id': bot_id, 
                                   'days': days,
                                   'limit': limit, 
                                   'action_channel': action_channel, 
                                   'no_channel': no_channel, 
                                   'selected_action': selected_action})
    return result.mappings().all()
  

def get_bot_channels(bot_id):
  with get_session() as session:
    sql = text("""
    WITH t0 AS (
    SELECT coalesce(channel,'') channel
    FROM app.bot_channels
    WHERE fid_owner = 788096
    ORDER BY id ASC
    ),

    t1 AS (
    SELECT coalesce(action_channel,'') channel,
    MAX(casted_at) last_post,
    count(distinct root_hash) bot_activity,
    avg(num_replies) avg_replies, 
    avg(num_likes) avg_likes,
    avg(num_recasts) avg_recasts,
    EXTRACT(EPOCH FROM (NOW() - MAX(casted_at))) / 3600 hours
    FROM app.bot_cast
    WHERE bot_id = 788096
    AND casted_at >= NOW() - INTERVAL '60 days'
    GROUP BY action_channel
    ORDER BY channel 	
    ),

    t2 AS (
    SELECT coalesce(channel_counts.channel,'') channel, SUM(num_casts) channel_activity
    FROM ds.channel_counts LEFT JOIN t1 on t1.channel=coalesce(channel_counts.channel,'')
    WHERE channel_counts.counted_at > t1.last_post
    GROUP BY channel_counts.channel
    ORDER BY channel 	
    )

    SELECT t0.channel, 
    t1.last_post, t1.hours, t1.bot_activity, t1.avg_replies, t1.avg_likes, t1.avg_recasts,
    t2.channel_activity
    FROM t0
    LEFT JOIN t1 on t0.channel=t1.channel
    LEFT JOIN t2 on t0.channel=t2.channel;
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    return result.mappings().all()


def get_bot_actions_stats_in_channel(bot_id, channel_id):
  with get_session() as session:
    sql = text("""
    WITH t0 AS (
    SELECT 
    selected_action action_class,
    max(casted_at) as last_cast,
    EXTRACT(EPOCH FROM (NOW() - MAX(casted_at))) / 3600 hours_ago           
    FROM app.bot_cast
    WHERE casted_at >= NOW() - INTERVAL '60 days' 
    AND bot_id=:bot_id
    AND action_channel=:channel_id
    AND cast_hash = root_hash
    AND selected_action is not NULL
    GROUP by selected_action
    )
    SELECT action_class, 
      hours_ago,
      (SELECT SUM(num_casts) FROM ds.channel_counts WHERE counted_at>t0.last_cast and channel=:channel_id) channel_activity 
    FROM t0
    """)
    result = session.execute(sql, {'bot_id': bot_id, 'channel_id': channel_id})
    return result.mappings().all()



def get_bot_actions_stats_no_channel(bot_id):
  with get_session() as session:
    sql = text("""
    SELECT 
    selected_action action_class,
    max(casted_at) as last_cast,
    EXTRACT(EPOCH FROM (NOW() - MAX(casted_at))) / 3600 hours_ago           
    FROM app.bot_cast
    WHERE casted_at >= NOW() - INTERVAL '60 days' 
    AND bot_id=:bot_id
    AND action_channel is NULL
    AND cast_hash = root_hash
    AND selected_action is not NULL
    GROUP by selected_action
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    return result.mappings().all()

def get_bot_prompts_stats(bot_id):
  with get_session() as session:
    sql = text("""
    SELECT action_prompt, action_channel,
        count(*) num_posts,
        avg(num_replies) avg_replies, 
        avg(num_likes) avg_likes,
        avg(num_recasts) avg_recasts,
        max(casted_at) last_post
    FROM app.bot_cast
    WHERE bot_id = :bot_id
    AND num_likes is not NULL
    AND casted_at >= NOW() - INTERVAL '30 days'
    GROUP BY action_prompt, action_channel
    ORDER BY avg(num_replies) + avg(num_likes) + avg(num_recasts) DESC
    LIMIT 50
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    return result.mappings().all()
  

def get_users_recently_praised(bot_id):
  with get_session() as session:
    sql = text("""
    SELECT DISTINCT selected_user as u FROM app.bot_cast WHERE bot_id = :bot_id AND selected_action='Praise' AND casted_at >= NOW() - INTERVAL '30 days'
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    rows = result.mappings().all()
    return [str(row['u']) for row in rows]
        

def get_random_user_to_praise(bot_id):
  with get_session() as session:
    sql = text("""
    WITH candidates as (
      SELECT DISTINCT username FROM ds.trending_casts WHERE timestamp >= NOW() - INTERVAL '5 days'
    ),
    exclude_users as (
      SELECT DISTINCT selected_user as u FROM app.bot_cast WHERE bot_id = :bot_id AND selected_action='Praise' AND casted_at >= NOW() - INTERVAL '30 days'
    )
    SELECT username FROM candidates WHERE username not in (SELECT u FROM exclude_users) ORDER BY random() LIMIT 1
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    row = result.mappings().fetchone()
    if row is not None:
      return row['username']
    else:
      return None
    

def get_random_user_to_praise_in_channel(bot_id, channel_url):
  df_top_users = get_top_daily_casters(channel_url, limit=20)
  df_top_users = df_top_users[df_top_users['fid'] != bot_id]
  top_users = df_top_users['User'].tolist()
  if len(top_users) == 0:
    return None
  recently_praised = get_users_recently_praised(bot_id)
  candidates = [user for user in top_users if user not in recently_praised]
  if len(candidates) == 0:
    return None
  return random.choice(candidates)
