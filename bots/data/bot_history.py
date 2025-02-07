from bots.data.pg import get_session
from sqlalchemy import text


def get_bot_casts_stats(bot_id):
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


def get_bot_recent_casts(bot_id):
  with get_session() as session:
    sql = text("""
    SELECT selected_action, action_prompt, action_channel, casted_text, casted_embeds, casted_at
    FROM app.bot_cast
    WHERE bot_id = :bot_id
    AND casted_at >= NOW() - INTERVAL '5 days'
    AND cast_hash = root_hash
    AND num_likes is NULL    
    AND casted_text is not NULL                  
    ORDER BY casted_at 
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    return result.mappings().all()


def get_bot_channels(bot_id):
  with get_session() as session:
    sql = text("""
    SELECT DISTINCT action_channel as channel
    FROM app.bot_cast 
    WHERE bot_id = :bot_id
    AND casted_at >= NOW() - INTERVAL '60 days'
    AND action_channel IS NOT NULL
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    return result.mappings().all()


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
