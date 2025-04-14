import random
from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.tools.parse import PARSE_TOOLS
from bots.tools.fetch import FETCH_TOOLS
from bots.tools.prepare import PREPARE_TOOLS
from bots.tools.helpers.tool_sequence import format_tool
from bots.tools.helpers.tool_sequence import clean_tools, compile_sequence


instructions_template = """
#TASK
You are @{{name}}, a social media bot programmed to do scheduled posts on a social media channel.
Given the provided context and instructions, your task is to select the tools that will help you prepare your next post.
You are provided with a list of available tools so that you know your possibilities.
Study the context and instructions carefully.
Then decide what you would like to post.
Then select the tools that will help you prepare your post.
Do not respond to the user, your task is only to plan the next tools to run.
Output 3 fields in json format: 
- intent: one word title for your plan
- intended_response_plan: what would you like to post?
- tools: the tools you need to prepare your post


#AVAILABLE TOOLS:
available_tools?

#OUTPUT FORMAT
{
  "intent": "...",
  "intended_response_plan": "your next post plan",
  "tools": "your list of selected tools, as a comma separated string"
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "intent":{"type":"STRING"},
    "intended_response_plan":{"type":"STRING"},
    "tools":{"type":"STRING"}
  }
}

fetch_tools = [
  'GetBotCastsInChannel',
  'GetBotCasts', 
  'GetCastsCategory', 
  'GetCastsChannel', 
  'GetCastsKeyword', 
  'GetCastsSearch', 
  'GetCastsUser', 
  'GetMoreLikeThis', 
  'GetNews', 
  'GetTrending', 
  'GetUserProfile', 
  'GetUserStats'
]
prepare_tools = [
  'CallPerplexity', 
  'CreateAvatar', 
  'CreateMostActiveUsersChart', 
  'CreateWordCloud', 
  'RenderFavoriteUsersTable'
]
fetch_tools_map = {x.name: x for x in FETCH_TOOLS if x.name in fetch_tools}
prepare_tools_map = {x.name: x for x in PREPARE_TOOLS if x.name in prepare_tools}
tool_map = {**fetch_tools_map, **prepare_tools_map}
available_tools = list(tool_map.values())


def select_intent(input):
  state = input.state
  instructions = state.format(instructions_template)
  available_tools_str = "\n".join([format_tool(tool) for tool in available_tools])
  instructions = instructions.replace('available_tools?', available_tools_str)
  prompt = state.format_all(succint=True)
  result = call_llm('medium', prompt, instructions, schema)
  intent = result['intent'] if 'intent' in result else ''
  response_plan = result['intended_response_plan'] if 'intended_response_plan' in result else ''
  targets = result['tools'] if 'tools' in result else ''
  tools = clean_tools(targets, tool_map)
  tools, log = compile_sequence(state, tools)
  return {
    'intent': intent, 
    'intended_targets': targets, 
    'intended_response_plan': response_plan,
    'todo': tools,
    'compile_log': log
  } 
  

IntentAssistant = Tool(
  name="IntentAssistant",
  description="Select current intent",
  metadata={
    'outputs': ['intent', 'intended_action_plan', 'intended_response_plan']
  },
  func=select_intent
) 
