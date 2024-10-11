import datetime 
from bots.data.pg import pg_connection


def get_channels():
  with pg_connection.cursor() as cursor:
    cursor.execute('SELECT id, name, url FROM ds.channels')
    return cursor.fetchall()
  

def get_channels_map():
  channels = get_channels()
  channels_by_id = {x[0].lower(): x[2] for x in channels}
  channels_by_name = {x[1].lower(): x[2] for x in channels}
  return channels_by_id, channels_by_name


def get_next_channel_digest():
  two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
  sql = f"""
  SELECT channels_digest.url, channels_digest.last_digest_at 
  FROM ds.channels_digest
  INNER JOIN ds.channels ON channels_digest.url = channels.url
  WHERE ((channels_digest.last_digest_at IS NULL) OR (channels_digest.last_digest_at < '{two_days_ago.strftime('%Y-%m-%d %H:%M:%S')}'))
  AND channels_digest.num_casts > 500
  AND channels.dsart_member = TRUE
  ORDER BY channels_digest.num_casts DESC
  LIMIT 1;
  """
  try:
    with pg_connection.cursor() as cursor:
      cursor.execute(sql)
      row = cursor.fetchone()
      return {
        'url': row[0],
        'last_digest_at': row[1]
      }
  except Exception as e:
    return None


def digested_channel(url):
  with pg_connection.cursor() as cursor:
    cursor.execute(
      "UPDATE ds.channels_digest SET last_digest_at = now(), num_casts = 0 WHERE url = %s",
      (url,)
    )
    pg_connection.commit()