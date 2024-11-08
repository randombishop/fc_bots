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

