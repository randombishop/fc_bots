from langchain.agents import Tool
from bots.utils.get_image_data import get_image_data
from bots.utils.llms2 import call_llm_with_image_url


instructions = """
#INSTRUCTIONS
You are provided with a profile picture from a social media user.
Describe the provided image in a short paragraph.
Focus on positive aspects in your description.
Keep your description concise, factual and to the point.
Include as many personal details as possible in your description, like gender, age, color or characteristic features.
Identify clues about their personality, interests, aesthetic preferences and include them in the description.
Also include any other detail that could be unique to this user. 
Your description should fit within standard safety policies and exclude prohibited words.
Please exclude anything related to violence, weapons, explicit content, nudity, self-harm, illegal activities, or hateful imagery.
Ensure that your description is suitable for a general audience.
Make sure you don't use " inside json strings. Avoid invalid json.
Output in json format.

#RESPONSE FORMAT:
{
  "image_description": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "image_description":{"type":"STRING"}
  }
}


def prepare(input):
  state = input.state
  llm = input.llm
  url = state.get('user_pfp_url')
  image_data = get_image_data(url)
  if image_data is None:
    return {'user_pfp_description': ''}
  prompt = "Describe the provided profile picture in a short paragraph."
  result = call_llm_with_image_url(llm, prompt, image_data, instructions, schema)
  description = result['image_description'] if 'image_description' in result else ''
  return {
    'user_pfp_description': description
  }


DescribePfp = Tool(
  name="DescribePfp",
  description="Describe a user's profile picture",
  metadata={
    'inputs': ['user_pfp_url'],
    'outputs': ['user_pfp_description']
  },
  func=prepare
)