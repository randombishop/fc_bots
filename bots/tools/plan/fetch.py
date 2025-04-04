from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.helpers.tool_sequence import clean_tools, compile_sequence, format_tool


select_tool_task = """
#TASK
You are @{{name}}, a social media bot on the farcaster platform.
Note that posts are called casts in farcaster.
You have access to a set of tools to fetch data before responding to your instructions.
Given the provided context and instructions, which tools should you run next?
You must only decide which tools will help you pull relevant data.
Do not pick multiple tools that fetch the same outputs.
Focus on the instructions intent and the parameters you already parsed to figure out which tools will provide useful context.
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

def format_tools():
  return "\n".join([format_tool(tool) for tool in FETCH_TOOLS])

def fetch(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all(succint=True)
  instructions = state.format(select_tool_task)
  instructions = instructions.replace('available_tools?', format_tools())
  result = call_llm(llm, prompt, instructions, select_tool_schema)
  tools= result['tools'] if 'tools' in result else None
  tools = clean_tools(tools, tool_map)
  tools, log = compile_sequence(state, tools, llm)
  ans = {
    'fetched': True,
    'fetch_tools': ','.join(tools),
    'fetch_log': log,
    'todo': tools
  }
  return ans
  

Fetch = Tool(
  name="Fetch",
  func=fetch,
  description="Fetch data before responding to the instructions"
)
