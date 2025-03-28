from langchain.agents import Tool
from bots.utils.llms2 import call_llm


instructions_template = """
#TASK
You are @{{name}}, a seasoned roast comedian known for your razor sharp wit and creative humor.
Your task is to roast @{{user_name}}.

#INSTRUCTIONS:
Analyze the posts provided from @{{user_name}} and craft a roast that is both hilarious and original.
Roast @{{user_name}} as hard as you can in one short but explosive tweet.
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
    "sentence1":{"type":"STRING"}
  }
}


def prepare_roast(input):
  state = input.state
  llm = input.llm
  df = state.df_casts_for_fid
  if df is None or len(df) == 0:
    raise Exception(f"Not enough activity to roast.")
  data = list(df['text'])
  text = "\n".join([str(x) for x in data])
  instructions = state.format(instructions_template.replace('{{user_name}}', state.user))
  result = call_llm(llm, text, instructions, schema)
  state.user_roast = result
  return {
    'user_roast': state.user_roast
  }


PrepareRoast = Tool(
  name="PrepareRoast",
  description="Generate a roast for the user",
  func=prepare_roast
)