import requests
from langchain.agents import Tool
from bots.utils.llms import call_llm_with_attachment


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


def get_pfp_description(input):
  state = input['state']
  if state.user_pfp_description is not None:
    return {'log': 'Already done.'}
  url = state.user_pfp_url
  if url is None or len(url) == 0:
    return {'log': 'No profile picture available.'}
  image_data = None
  mime_type = None
  try:  
    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    image_data = response.content
    mime_type = response.headers['Content-Type']
  except Exception as e:
    return {'log': f'Error fetching profile picture: {e}'}
  if image_data is None or mime_type is None:
    return {'log': 'Could not obtain image data and mime type.'}
  prompt = "Describe the provided profile picture in a short paragraph."
  result = call_llm_with_attachment(prompt, image_data, mime_type, instructions, schema)
  if 'image_description' not in result:
    return {'log': 'Could not generate an image description.'}
  description = result['image_description']
  state.user_pfp_description = description
  return {
    'user_pfp_description': state.user_pfp_description
  }


GetPfpDescription = Tool(
  name="get_pfp_description",
  description="Get the description of a profile picture",
  func=get_pfp_description
)