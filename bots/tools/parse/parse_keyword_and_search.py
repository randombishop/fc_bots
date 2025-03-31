from langchain.agents import Tool
from bots.utils.llms2 import call_llm
from bots.utils.read_params import read_keyword, read_string


instructions_template = """
#TASK
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
Output your response in the following json format.

#RESPONSE FORMAT
{
  "keyword": "...",
  "search": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "keyword":{"type":"STRING"},
    "search":{"type":"STRING"}
  }
}


def parse(input):
  state = input.state
  llm = input.llm
  prompt = state.format_all()
  instructions = state.format(instructions_template)
  params = call_llm(llm, prompt, instructions, schema)
  search = read_string(params, key='search', max_length=500)
  keyword = read_keyword(params)
  reasoning = read_string(params, key='reasoning')
  return {
    'search': search,
    'keyword': keyword
  }


ParseKeywordAndSearch = Tool(
  name="ParseKeywordAndSearch",
  description="Set parameters search and keyword to pull more data.",
  metadata={
    'outputs': ['search', 'keyword']
  },
  func=parse
)