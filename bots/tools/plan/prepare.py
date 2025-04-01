from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.plan.tool_sequence import filter_tools, compile_sequence, format_tool


select_tool_task = """
#TASK
You are @{{name}}, a social media bot on the farcaster network.
Note that posts are called casts on farcaster.
You have access to a set of tools before responding to your instructions.
Your can use your tools to pre-process data, generate images, charts, tables, wordclouds, etc.
Given the provided context and instructions, which tools would be helpful to enrich your response?
You must only decide which tools will help you improve your response.
Only select tools if they are clearly relevant to the instructions and will be helpful.
If you already have all the context you need to fully respond to the instructions, return an empty list.

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

tool_map = {x.name: x for x in PREPARE_TOOLS}

def format_tools():
  return "\n".join([format_tool(tool) for tool in PREPARE_TOOLS])

def prepare(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all(succint=True)
  instructions = state.format(select_tool_task)
  instructions = instructions.replace('available_tools?', format_tools())
  result = call_llm(llm, prompt, instructions, select_tool_schema)
  tools = result['tools'] if 'tools' in result else None
  tools = filter_tools(tools, tool_map)
  tools, log = compile_sequence(state, tools, llm)
  ans = {
    'prepared': True,
    'prepare_tools': ','.join(tools),
    'prepare_log': log,
    'todo': tools
  }
  return ans
  
  
Prepare = Tool(
  name="Prepare",
  func=prepare,
  description="Prepare data before responding to the instructions"
)
