import os
import json
from bots.v2.bot2 import Bot2
from langchain.agents import AgentExecutor

bot_id = int(os.getenv('TEST_BOT'))

  
def run_bot(input):
    input['bot_id'] = bot_id
    bot = Bot2()
    executor = AgentExecutor(agent=bot, tools=bot._tools, llm=bot._llm)
    executor.invoke(input=json.dumps(input), config={"run_name": "test1"})
    bot._state.debug()
