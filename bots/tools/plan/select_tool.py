from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS


select_tool_task = """
#TASK
You are @{{name}}, a social media bot with access to a set of tools.
Given the provided context and instructions, which tool should you run next?
Your goal is not to respond to the instructions at this point, you must only decide which tool to execute to gain more data.
Decide the tool that should be used before responding to the instructions.
The tools use parameters from the current context so make sure their parameters are set before calling them.
When you have gathered enough data to respond to the instructions, respond with {"tool": null, "ready": true}
If you can't figure out how to respond and none of tools would help further, respond with {"tool": null, "ready": false}
If you want to run a tool, respond with {"tool": "...", "ready": false}
Also provide a reasoning for your choice.

#AVAILABLE TOOLS

## For setting parameters

parse_tools?

## For fetching your data

fetch_tools?

## For processing your data

prepare_tools?


#OUTPUT FORMAT
{
  "tool": "...",
  "ready": true|false,
  "reasoning": "..."
}
"""

select_tool_schema = {
  "type":"OBJECT",
  "properties":{
    "tool":{"type":"STRING"},
    "ready":{"type":"BOOLEAN"},
    "reasoning":{"type":"STRING"}
  }
}

def format_tools(list):
  return '\n'.join([f"##{x.name}\nDescription: {x.description}\n" for x in list])


def select_tool(input):
  state = input.state
  llm = input.llm
  if state.instructions is None or len(state.instructions) == 0:
    raise Exception('No instructions provided')
  prompt = state.format_tools_log()
  instructions = state.format(select_tool_task)
  instructions = instructions.replace('parse_tools?', format_tools(PARSE_TOOLS))
  instructions = instructions.replace('fetch_tools?', format_tools(FETCH_TOOLS))
  instructions = instructions.replace('prepare_tools?', format_tools(PREPARE_TOOLS))
  result = call_llm(llm, prompt, instructions, select_tool_schema)
  state.tools_done = True
  return {
    'tool': result['tool'], 
    'ready': result['ready'],
    'reasoning': result['reasoning']
  }
  

SelectTool = Tool(
  name="SelectTool",
  func=select_tool,
  description="Select the next tool to run"
)
