from sqlalchemy import Table
from bots.data.pg import engine, metadata, get_session

bot_channels_table = Table('bot_channels', metadata, autoload_with=engine, schema='app')
bot_prompts_table = Table('bot_prompts', metadata, autoload_with=engine, schema='app')


def get_bot_channels(bot_id):
  with get_session() as session:
    stmt = bot_channels_table.select().where(
      bot_channels_table.c.fid_owner == bot_id,
      bot_channels_table.c.channel != None
    ).order_by(bot_channels_table.c.channel)
    result = session.execute(stmt).mappings().fetchall()
    return result

def get_bot_prompt(id):
  with get_session() as session:
    stmt = bot_prompts_table.select().where(bot_prompts_table.c.id == id)
    result = session.execute(stmt).mappings().fetchone()
    return result
  
def get_bot_prompts(bot_id):
  with get_session() as session:
    stmt = bot_prompts_table.select().where(bot_prompts_table.c.bot_id == bot_id)
    result = session.execute(stmt).mappings().fetchall()
    return result
  
  
