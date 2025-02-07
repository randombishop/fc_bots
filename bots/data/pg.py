import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


DATABASE_URL = os.getenv('DATABASE_URL')
engine = None
metadata = None
SessionLocal = None
if DATABASE_URL is not None:
  engine = create_engine(DATABASE_URL)
  metadata = MetaData()
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def is_postgres_enabled():
  return DATABASE_URL is not None and SessionLocal is not None

@contextmanager
def get_session():
  if not is_postgres_enabled():
    raise Exception("Postgres is not enabled")
  session = SessionLocal()
  try:
    yield session
    session.commit()
  except Exception:
    session.rollback()
    raise
  finally:
    session.close()
