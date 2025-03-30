from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.plan.tool_sequence import compile_sequence


select_tool_task = """
#TASK
You are @{{name}}, a social media bot with access to a set of tools to fetch data before responding to your instructions.
Given the provided context and instructions, which tools should you run next?
You must only decide which tools will help you pull relevant data.
Do not pick multiple tools that fetch the same outputs.

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


def format_tool(tool):
  return f"{tool.name}: {tool.description} -> [{', '.join(tool.metadata['outputs'])}]"

def format_tools():
  return "\n".join([format_tool(tool) for tool in FETCH_TOOLS])

def fetch(input):
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
    'fetch_tools_llm': tools_llm,
    'fetch_tools': tools
  }
  for t in tools:
    tool = tool_map[t]
    result = tool.invoke({'input': input})
    ans.update(result)
  state.fetched = True
  return ans
  
  
Fetch = Tool(
  name="Fetch",
  func=fetch,
  description="Fetch data before responding to the instructions"
)
