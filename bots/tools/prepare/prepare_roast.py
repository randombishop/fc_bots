from langchain.agents import Tool
from bots.utils.llms2 import call_llm


instructions_template = """
#TASK
You are @{{name}}, a seasoned roast comedian known for your razor sharp wit and creative humor.
Your task is to roast @{{user}}.

#INSTRUCTIONS:
Analyze the posts provided from @{{user}} and craft a roast that is both hilarious and original.
Roast @{{user}} as hard as you can in one short but explosive tweet.
Cleverly highlight the quirky, absurd, or contradictory elements in the posts.
Use wordplay, irony, and playful sarcasm.
Maintain a humorous, light-hearted tone without resorting to unnecessarily mean-spirited personal attacks.
Be respectful, and do not use sexual, religious or political references.
Output the result in json format.
Make sure you don't use " inside json strings. Avoid invalid json.
Output one single tweet in json format.

#RESPONSE FORMAT:
{
  "tweet": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "tweet":{"type":"STRING"}
  }
}


def prepare(input):
  state = input.state
  llm = input.llm
  prompt = state.get('casts_user')
  instructions = state.format(instructions_template)
  result = call_llm(llm, prompt, instructions, schema)
  if 'tweet' not in result:
    raise Exception(f"Roast tool returned invalid result")
  text = result['tweet']
  return {
    'user_roast': text
  }


PrepareRoast = Tool(
  name="PrepareRoast",
  description="Generate a roast for the user",
  metadata={
    'inputs': ['casts_user'],
    'outputs': ['user_roast']
  },
  func=prepare
)