import os
import psycopg2


DATABASE_URL = os.getenv('DATABASE_URL')
connection = psycopg2.connect(DATABASE_URL)

def get_channels():
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, name, url FROM ds.channels')
        channels = cursor.fetchall()
    channels_by_id = {x[0].lower(): x[2] for x in channels}
    channels_by_name = {x[1].lower(): x[2] for x in channels}
    return channels_by_id, channels_by_name
