import os
import json
from bots.bot import Bot
from langchain.agents import AgentExecutor

bot_id = int(os.getenv('TEST_BOT'))

  
def run_bot(test_id, request=None, fid_origin=None, parent_hash=None, attachment_hash=None, root_parent_url=None, selected_channel=None, selected_action=None):
    input = {
        'bot_id': bot_id,
        'request': request,
        'fid_origin': fid_origin,
        'parent_hash': parent_hash,
        'attachment_hash': attachment_hash,
        'root_parent_url': root_parent_url,
        'selected_channel': selected_channel,
        'selected_action': selected_action
    }
    bot = Bot()
    executor = AgentExecutor(agent=bot, tools=bot._tools, llm=bot._llm)
    executor.invoke(input=json.dumps(input), config={"run_name": test_id})
    bot._state.debug()
    return bot._state
