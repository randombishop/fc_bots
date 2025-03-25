from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_keyword, read_string


prompt_template = """
#WHAT IS TRENDING IN GENERAL (NOT SPECIFIC TO THE CHANNEL)
{{trending}}

#RECENT POSTS IN THE CHANNEL
{{casts_in_channel}}

#WHAT YOU RECENTLY POSTED IN THE CHANNEL
{{bot_casts_in_channel}}

#INSTRUCTIONS
{{instructions}}
"""


instructions_template = """
You are @{{name}}, a social media bot.

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#YOUR STYLE
{{style}}

#CURRENT CHANNEL
{{channel}}

#TASK
You are provided with a data sample from the farcaster social media platform, plus some current instructions.
First, study the provided data and understand your instructions.
Before processing your instructions, you can access data from the social media platform to prepare a good post.
You have access to an API that can pull data based on a search phrase or a keyword.
Your goal is not to execute your instructions at this point, you must only come up with an interesting search phrase and a keyword to call the API twice.
Your goal is to propose a search phrase and a keyword to gain access to more data before responding.
Make the search phrase specific to the instructions intent.
Make the keyword generic so that it generates many matches, pull broader context, and see the bigger picture.
Do not use abbreviation for the keyword, it has to be at least 4 characters long.
The keyword should be a single word, not a phrase.
The keyword should be very different from the search phrase and open an original perspective on the instructions.
Please also explain why you picked your search phrase and keyword.
Output your response in the following json format.

#RESPONSE FORMAT
{
  "keyword": "...",
  "search": "...",
  "reasoning": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "keyword":{"type":"STRING"},
    "search":{"type":"STRING"},
    "reasoning":{"type":"STRING"}
  }
}


def parse_instructions_params(input):
  state = input.state
  llm = input.llm
  if not state.should_continue:
    return {'log': 'Not fetching data because should_continue is false'}
  prompt = state.format(prompt_template)
  instructions = state.format(instructions_template)
  params = call_llm(llm, prompt, instructions, schema)
  state.search = read_string(params, key='search', max_length=500)
  state.keyword = read_keyword(params)
  state.params_reasoning = read_string(params, key='reasoning')
  state.max_rows = 25
  return {
    'search': state.search,
    'keyword': state.keyword,
    'params_reasoning': state.params_reasoning,
    'max_rows': state.max_rows
  }


ParseInstructionsParams = Tool(
  name="ParseInstructionsParams",
  func=parse_instructions_params,
  description="Parse search phrases to pull more data"
)