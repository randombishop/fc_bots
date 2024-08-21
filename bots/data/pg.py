import os
import psycopg2


url = os.getenv('DATABASE_URL')
pg_connection = psycopg2.connect(url)

