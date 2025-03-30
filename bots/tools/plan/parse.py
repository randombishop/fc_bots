from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.parse import PARSE_TOOLS


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
  prompt = state.format_conversation()
  instructions = state.format(select_tool_task)
  instructions = instructions.replace('available_tools?', format_tools())
  result = call_llm(llm, prompt, instructions, select_tool_schema)
  state.parsed = True
  return result
  
  
Parse = Tool(
  name="Parse",
  func=parse,
  description="Parse parameters for next tools"
)
