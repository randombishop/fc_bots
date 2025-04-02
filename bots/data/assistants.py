from sqlalchemy import Table
from bots.data.pg import engine, metadata, get_session

bot_prompts_table = Table('bot_prompts', metadata, autoload_with=engine, schema='app')


def get_bot_prompt(id):
  with get_session() as session:
    stmt = bot_prompts_table.select().where(bot_prompts_table.c.id == id)
    result = session.execute(stmt).mappings().fetchone()
    return result
