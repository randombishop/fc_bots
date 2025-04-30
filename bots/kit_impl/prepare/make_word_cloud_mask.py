from langchain.agents import Tool
import os
import uuid
import requests
from bots.utils.llms2 import generate_image
from PIL import Image, ImageEnhance, ImageOps


prompt_template = """
Generate an image with a pure white background and a single, bold colored shape to illustrate this text: 
"{{text}}"
The shape should be highly symbolic and abstract, maximizing canvas coverage while leaving minimal white background space. 
The shape should be smooth, well-defined, and simple. 
Avoid gradients or fine details, your design should be recognizable from a distance.
"""


def prepare(input):
  state = input.state
  text = state.get('wordcloud_text')
  if text is None or len(text)==0:
    raise Exception("No text to generate mask")
  # Generate a new image
  prompt = prompt_template.replace("{{text}}", text)
  image_url = generate_image(prompt)
  key = str(uuid.uuid4())
  file1 = key+'.original.png'
  response = requests.get(image_url)
  response.raise_for_status()
  with open(file1, 'wb') as f:
    f.write(response.content)
  # Convert to mask with white background
  img = Image.open(file1)
  img = img.convert('RGB')
  pixels = img.load()
  width, height = img.size
  print('Image size', width, height)
  mask = Image.new('RGB', (width, height))
  mask_pixels = mask.load()
  threshold = 180
  push = 360
  for x in range(width):
    for y in range(height):
      r, g, b = pixels[x, y]
      brightness = (r + g + b) // 3
      if brightness > threshold:
        mask_pixels[x, y] = (255, 255, 255)
      else:
        r = min(240, int((r + push) * 240 // (240 + push)))
        g = min(240, int((g + push) * 240 // (240 + push)))
        b = min(240, int((b + push) * 240 // (240 + push)))
        mask_pixels[x, y] = (r, g, b)
  # Create darkened background image
  img_dark = ImageOps.invert(img)
  enhancer = ImageEnhance.Brightness(img_dark)
  img_dark = enhancer.enhance(0.15)
  img_dark = img_dark.convert("RGBA")
  os.remove(file1)
  return {
    'wordcloud_mask': mask,
    'wordcloud_background': img_dark,
    'wordcloud_width': width,
    'wordcloud_height': height
  }

MakeWordCloudMask = Tool(
  name="MakeWordCloudMask",
  description="Make a wordcloud mask to be used as a wordcloud background",
  metadata={
    'inputs': ['wordcloud_text'],
    'outputs': ['wordcloud_mask', 'wordcloud_background', 'wordcloud_width', 'wordcloud_height']
  },
  func=prepare
)
