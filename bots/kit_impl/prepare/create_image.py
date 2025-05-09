import os
import uuid
import requests
from bots.kit_interface.image import Image
from bots.kit_interface.bio import Bio
from bots.kit_interface.lore import Lore
from bots.utils.llms2 import call_llm, generate_image
from bots.utils.gcs import upload_to_gcs
from bots.utils.format_state import format_template


instructions_template = """
You are @{{bot_name}}

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#TASK
Your task is to prepare a prompt for dall-e3 model so we can generate a new image.
Based on the current context and instructions, prepare a prompt for dall-e3 model to generate an image that can be used in your posts.
Your prompt should follow dall-e3 best practices and yield a unique, creative and beautiful image.
Most importantly, your prompt should generate an image that will fit the purpose of the posts you're preparing.
Focus on your post goal as you compose your image prompt.
Your prompt should fit within standard safety policies.
Please exclude anything related to violence, weapons, explicit content, nudity, self-harm, illegal activities, or hateful imagery.
Ensure that your prompt is suitable for a general audience.
Avoid any prohibited keywords and make sure that your prompt will not be rejected by the image generation model.
Make sure you don't use " inside json strings. Avoid invalid json.
Output 1 sentence in json format.

#RESPONSE FORMAT:
{
  "image_prompt": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "image_prompt":{"type":"STRING"}
  }
}


def create_image(context: str, bot_name: str, bio: Bio, lore: Lore) -> Image:
  prompt = context
  instructions = format_template(instructions_template, {
    'bot_name': bot_name,
    'bio': bio,
    'lore': lore
  })
  result = call_llm('medium', prompt, instructions, schema)
  image_prompt = result['image_prompt'] if 'image_prompt' in result else None
  image_url = generate_image(image_prompt)
  filename = str(uuid.uuid4())+'.png'
  response = requests.get(image_url)
  response.raise_for_status()
  with open(filename, 'wb') as f:
    f.write(response.content)
  upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
  os.remove(filename)
  image_url = f"https://fc.datascience.art/bot/main_files/{filename}"
  return Image(image_prompt, image_url)
