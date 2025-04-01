from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.parse import PARSE_TOOLS
from bots.tools.helpers.tool_sequence import clean_tools, compile_sequence, format_tool


select_tool_task = """
#TASK
You are @{{name}}, a social media bot with access to a set of tools.
Given the provided context and instructions, which parsers should we run first?
You will run other tools later to fetch and prepare your response.
For now, focus only on the parameters that you will need and select the best parsers to set them.
You can select one or multiple parsers if needed.

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

tool_map = {x.name: x for x in PARSE_TOOLS}

def format_tools():
  return "\n".join([format_tool(tool) for tool in PARSE_TOOLS])

def parse(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all(succint=True)
  instructions = state.format(select_tool_task)
  instructions = instructions.replace('available_tools?', format_tools())
  result = call_llm(llm, prompt, instructions, select_tool_schema)
  tools = result['tools'] if 'tools' in result else None
  tools = clean_tools(tools, tool_map)
  tools, log = compile_sequence(state, tools, llm)
  ans = {
    'parsed': True,
    'parse_tools': ','.join(tools),
    'parse_log': log,
    'todo': tools,
  }
  return ans
  
  
Parse = Tool(
  name="Parse",
  func=parse,
  description="Parse parameters for next tools"
)
