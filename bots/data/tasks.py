from bots.data.pg import pg_connection


def create_app_user_if_not_exists(fid):
  with pg_connection.cursor() as cursor:
    cursor.execute("SELECT * FROM app.app_user WHERE fid = %s", (fid,))
    if cursor.fetchone() is None:
      cursor.execute("INSERT INTO app.app_user (fid) VALUES (%s)", (fid,))
      pg_connection.commit()


def get_credits(fid):
  with pg_connection.cursor() as cursor:
    cursor.execute("SELECT credits FROM app.app_user WHERE fid = %s", (fid,))
    return cursor.fetchone()[0]

  
def deduct_credits(fid, cost):
  with pg_connection.cursor() as cursor:
    cursor.execute("UPDATE app.app_user SET credits = credits - %s WHERE fid = %s", (cost, fid))
    pg_connection.commit()