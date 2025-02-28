import requests
from bots.i_prepare_step import IPrepareStep
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

class GetPfpDescrition(IPrepareStep):
    
  def prepare(self):
    if self.state.user_pfp_description is not None:
      return
    url = self.state.user_pfp_url
    if url is None or len(url) == 0:
      self.state.log += 'No profile picture available.\n'
      return
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
      self.state.log += f'<GetPfpDescrition>Error fetching profile picture: {e}</GetPfpDescrition>\n'
      return
    if image_data is None or mime_type is None:
      self.state.log += '<GetPfpDescrition>Could not obtain image data and mime type.</GetPfpDescrition>\n'
      return
    prompt = "Describe the provided profile picture in a short paragraph."
    result = call_llm_with_attachment(prompt, image_data, mime_type, instructions, schema)
    if 'image_description' not in result:
      self.state.log += '<GetPfpDescrition>Could not generate an image description.</GetPfpDescrition>\n'
      return
    description = result['image_description']
    self.state.user_pfp_description = description
    log = '<GetPfpDescrition>\n'
    log += f'url: {url}\n'
    log += f'mime_type: {mime_type}\n'
    log += f'image_data: {len(image_data)}\n'
    log += f'image_description: {description}\n'
    log += '</GetPfpDescrition>\n'
    self.state.log += log
