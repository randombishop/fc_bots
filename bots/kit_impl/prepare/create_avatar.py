import os
import uuid
import requests
from bots.kit_interface.user_id import UserId
from bots.kit_interface.user_profile import UserProfile
from bots.kit_interface.image_description import ImageDescription
from bots.kit_interface.user_casts_description import UserCastsDescription
from bots.kit_interface.avatar import Avatar
from bots.utils.llms2 import call_llm, generate_image
from bots.utils.gcs import upload_to_gcs
from bots.utils.prompts import format_template


prompt_template = """
# USER
@{{user_name}}

# USER DISPLAY NAME
{{user_display_name}}

# USER BIO
{{user_bio}}

# USER PFP DESCRIPTION
{{user_pfp_description}}

# USER CASTS
{{casts_user}}
"""

instructions_template = """
You are @{{name}}

#YOUR BIO
{{bio}}

#YOUR LORE
{{lore}}

#TASK
Your task is to prepare a prompt for dall-e3 model so we can generate an avatar for @{{user}}.

#INSTRUCTIONS:
The posts provided are all from @{{user}}. 
Analyze their posts carefully.
Identify clues about their personality, interests, aesthetic preferences, and how they express themselves.
Make your best guess at @{{user}}'s:
**Gender**: Pick either male or female even if you are not sure, it will be funny if you miss.
**Age**: If you gathered a clue, make a smart guess, otherwise make a a wild guess. You can even make them a baby or very old person for fun. 
**Style**: Do they lean toward minimalism, maximalism, cyberpunk, vintage, fantasy, surrealism, or something else?
**Color Palette**: Do they mention colors, moods, or artistic inspirations? Incorporate these.
**Art Style**: Pick the artistic technique that best fits with their vibe. (e.g., "oil painting with bold brushstrokes," "digital illustration with neon highlights," or "Japanese woodblock print aesthetics", these are just examples, you are encouraged to propose anything here...)
**Themes & Motifs**: Symbols, references, or concepts that would make the avatar feel unique.
Your prompt should include a gender, age, style, a color palette, an artistic technique, themes and motifs.
Include any other relevant details to make the avatar unique and tailored to @{{user}}.
Focus in their profile picture description, and use it to make the avatar a re-invention of their profile picture but with the same core and spirit.
Your goal is to create an avatar prompt that makes @{{user}} feel truly seen and celebrated, a parallel to their orginial profile picture but with your magic.
The avatar prompt should have **artistic depth**, **aesthetic coherence**, and a unique **visual identity** that matches @{{user}}.
The generator will only receive your prompt and won't have access to the original picture, so make it a self sufficient prompt.
Do not include a reference to original profile picture like "mirroring the original pfp" - Instead, specify exactly what you want to mirror from it.
Your prompt should fit within standard safety policies.
Please exclude anything related to violence, weapons, explicit content, nudity, self-harm, illegal activities, or hateful imagery.
Ensure that your prompt is suitable for a general audience.
Avoid any prohibited keywords and make sure that your prompt will not be rejected by the image generation model.
Make sure you don't use " inside json strings. Avoid invalid json.
Output 1 sentence in json format.

#RESPONSE FORMAT:
{
  "avatar_prompt": "..."
}
"""

schema = {
  "type":"OBJECT",
  "properties":{
    "avatar_prompt":{"type":"STRING"}
  }
}


def create_avatar(bot_name: str, bio: Bio, lore: Lore, user_id: UserId, user_profile: UserProfile, pfp_description: ImageDescription, casts_description: UserCastsDescription) -> Avatar:
  prompt = format_template(prompt_template, {
    'user_name': user_id.username,
    'user_display_name': user_profile.display_name,
    'user_bio': user_profile.bio,
    'user_pfp_description': pfp_description.description,
    'casts_user': casts_description.text
  })
  if len(prompt) < 100:
    return {'log': 'Not enough data to generate a prompt for avatar'}
  instructions = format_template(instructions_template, {
    'name': bot_name,
    'bio': bio,
    'lore': lore
  })
  result = call_llm('medium', prompt, instructions, schema)
  user_avatar_prompt = result['avatar_prompt'] if 'avatar_prompt' in result else None
  image_url = generate_image(user_avatar_prompt)
  filename = str(uuid.uuid4())+'.png'
  response = requests.get(image_url)
  response.raise_for_status()
  with open(filename, 'wb') as f:
    f.write(response.content)
  upload_to_gcs(local_file=filename, target_folder='png', target_file=filename)
  os.remove(filename)
  user_avatar = f"https://fc.datascience.art/bot/main_files/{filename}"
  return Avatar(user_avatar_prompt, user_avatar)
