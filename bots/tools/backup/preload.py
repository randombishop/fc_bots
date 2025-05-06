from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.helpers.tool_sequence import filter_suggested_tools, clean_tools, format_tool


select_tool_task = """
#TASK
You are @{{name}}, a social media bot on the farcaster platform.
Note that posts are called casts in farcaster.
Before planning your actions and response, you have a access to a first series of tools that do not require any parameter.
You can run them if you would like to gain access to preliminary data such as globally trending posts, your previous posts, channel activity, etc.
Avoid calling tools if you don't see a clear benefit as they can slow your response time unnecessarily.
If none of the proposed tools would be useful for your next steps, you can skip this step and return an empty list.
Do not respond to the user, your task is only to select the next tools to run.

#AVAILABLE TOOLS
available_tools?

#OUTPUT FORMAT
{
  "tools": "comma separated list of tools to execute next"
}
"""

select_tool_schema = {
  "type":"OBJECT",
  "properties":{
    "tools":{"type":"STRING"}
  }
}

tool_map = {x.name: x for x in FETCH_TOOLS}

def preload(input):
  state = input.state
  available_data = state.get_available_data()
  available_tool_names = filter_suggested_tools([x.name for x in FETCH_TOOLS], available_data)
  available_tools = [tool_map[x] for x in available_tool_names]
  if len(available_tools) == 0:
    return {
      'preloaded': True,
      'preload_tools': '',
      'todo': []
    }
  available_tools = "\n".join([format_tool(t) for t in available_tools])
  prompt = state.format_conversation()
  instructions = state.format(select_tool_task)
  instructions = instructions.replace('available_tools?', available_tools)
  result = call_llm('medium', prompt, instructions, select_tool_schema)
  tools = result['tools'] if 'tools' in result else None
  tools = clean_tools(tools, available_tool_names)
  ans = {
    'preloaded': True,
    'preload_tools': ','.join(tools),
    'todo': tools
  }
  return ans
  

Preload = Tool(
  name="Preload",
  func=preload,
  description="Load initial data that do not require any parameter parsing"
)
