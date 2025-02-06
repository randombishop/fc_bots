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
    LIMIT 100
    """)
    result = session.execute(sql, {'bot_id': bot_id})
    return result.mappings().all()


def get_channel_summaries(bot_id):
  with get_session() as session:
    sql = text("""
    SELECT DISTINCT ON (action_channel) 
      action_channel AS channel, 
      casted_text AS text,
      casted_at AS timestamp
    FROM app.bot_cast
    WHERE bot_id = :bot_id
      AND action_prompt LIKE 'Summarize channel /%'
      AND casted_at >= NOW() - INTERVAL '30 days'
      AND casted_text IS NOT NULL
      AND cast_hash = root_hash
    ORDER BY action_channel, casted_at DESC;
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
