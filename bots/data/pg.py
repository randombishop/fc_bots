import os
import psycopg2


DATABASE_URL = os.getenv('DATABASE_URL')
pg_connection = psycopg2.connect(DATABASE_URL)


    