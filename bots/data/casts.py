from bots.data.pg import get_session
from sqlalchemy import text


def get_trending_casts(limit=100):
  with get_session() as session:
    sql = text("""
    SELECT *
    FROM ds.trending_casts
    ORDER BY timestamp DESC
    LIMIT :limit
    """)
    result = session.execute(sql, {'limit': limit})
    return result.mappings().all()
  

