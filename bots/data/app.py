from bots.data.pg import engine, metadata, get_session
from sqlalchemy import Table, select



bot_character_table = Table('bot_character', metadata, autoload_with=engine, schema='app')


def get_bot_character(fid_owner):
  with get_session() as session:
    stmt = select(bot_character_table).where(bot_character_table.c.fid_owner == fid_owner)
    row = session.execute(stmt).mappings().fetchone()
    return row['character']