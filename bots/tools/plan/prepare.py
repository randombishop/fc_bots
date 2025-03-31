from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.plan.tool_sequence import compile_sequence, format_tool


select_tool_task = """
#TASK
You are @{{name}}, a social media bot with access to a set of tools before responding to your instructions.
Your can use your tools to pre-process data, generate images, charts, tables, wordclouds, etc.
 Given the provided context and instructions, which tools would be helpful to enrich your response?
You must only decide which tools will help you improve your response.

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
  available_data = state.get_available_data()
  prompt = state.format_all()
  instructions = state.format(select_tool_task)
  instructions = instructions.replace('available_tools?', format_tools())
  result = call_llm(llm, prompt, instructions, select_tool_schema)
  tools_llm = result['tools'] if 'tools' in result else None
  tools = compile_sequence(tools_llm, available_data)
  ans = {
    'prepared': True,
    'prepare_tools_llm': tools_llm,
    'prepare_tools_sequence': ','.join(tools),
    'todo': tools
  }
  return ans
  
  
Prepare = Tool(
  name="Prepare",
  func=prepare,
  description="Prepare data before responding to the instructions"
)
