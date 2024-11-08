import json
from bots.data.pg import pg_connection

  
def get_task(task_id):
  with pg_connection.cursor() as cursor:
    cursor.execute('SELECT * FROM ds.tasks WHERE id = %s', (task_id,))
    return cursor.fetchone()


def update_task_result(task_id, result):
  with pg_connection.cursor() as cursor:
    cursor.execute(
      "UPDATE ds.tasks SET result = %s, done_at = now() WHERE id = %s",
      (json.dumps(result), task_id)
    )
    pg_connection.commit()


def get_mention_listener_next_page(fid):
  with pg_connection.cursor() as cursor:
    cursor.execute('SELECT next_page FROM ds.mention_listeners WHERE target_id = %s', (fid,))
    rows = cursor.fetchall()
    if len(rows) == 0:
      return None
    else:
      return rows[0][0]
    

def update_mention_listener_next_page(fid, next_page):
  with pg_connection.cursor() as cursor:
    cursor.execute('UPDATE ds.mention_listeners SET next_page = %s WHERE target_id = %s', (next_page, fid))
    pg_connection.commit()