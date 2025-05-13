from bots.kit_interface.user_info import UserInfo
from bots.kit_interface.image_description import ImageDescription
from bots.utils.get_url_data import get_url_data
from bots.utils.llms2 import call_llm_with_data


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


def describe_pfp(user_info: UserInfo) -> ImageDescription:
  url = user_info.pfp_url
  data, mime_type = get_url_data(url)
  if data is None or mime_type is None:
    return {'user_pfp_description': ''}
  prompt = "Describe the provided profile picture in a short paragraph."
  result = call_llm_with_data(prompt, data, mime_type, instructions, schema)
  description = result['image_description'] if 'image_description' in result else ''
  return ImageDescription(url, description)

