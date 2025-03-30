from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.parse import PARSE_TOOLS
from bots.tools.plan.tool_sequence import compile_sequence


select_tool_task = """
#TASK
You are @{{name}}, a social media bot with access to a set of tools.
Given the provided context and instructions, which parsers should we start by running?
You must only decide which tools to execute, so that we have parameters ready for next tools that will pull and prepare your data.
Do not pick multiple tools that set the same output.

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


def format_tool(tool):
  return f"{tool.name}: {tool.description} -> [{', '.join(tool.metadata['outputs'])}]"

def format_tools():
  return "\n".join([format_tool(tool) for tool in PARSE_TOOLS])

def parse(input):
  state = input.state
  llm = input.llm
  available_data = state.get_available_data()
  prompt = state.format_conversation()
  instructions = state.format(select_tool_task)
  instructions = instructions.replace('available_tools?', format_tools())
  result = call_llm(llm, prompt, instructions, select_tool_schema)
  tools_llm = result['tools'] if 'tools' in result else None
  tools = compile_sequence(tools_llm, available_data)
  ans = {
    'parse_tools_llm': tools_llm,
    'parse_tools': tools
  }
  for t in tools:
    tool = tool_map[t]
    result = tool.invoke({'input': input})
    ans.update(result)
  state.parsed = True
  return ans
  
  
Parse = Tool(
  name="Parse",
  func=parse,
  description="Parse parameters for next tools"
)
