import datetime 
from bots.data.pg import pg_connection


def get_next_category_digest():
  sql = f"""
  SELECT category, last_digest_at 
  FROM ds.category_digest
  WHERE ((last_digest_at IS NULL) OR (EXTRACT(EPOCH FROM (NOW() - last_digest_at)) / 3600 > min_interval))
  ORDER BY last_digest_at
  LIMIT 1;
  """
  try:
    with pg_connection.cursor() as cursor:
      cursor.execute(sql)
      row = cursor.fetchone()
      return {
        'category': row[0],
        'last_digest_at': row[1]
      }
  except Exception as e:
    return None


def digested_category(category):
  with pg_connection.cursor() as cursor:
    cursor.execute(
      "UPDATE ds.category_digest SET last_digest_at = now() WHERE category = %s",
      (category,)
    )
    pg_connection.commit()