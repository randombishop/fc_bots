from openai import OpenAI

def generate_image(prompt):
  try:
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url
  except Exception as e:
    print('openai image generation failed for following prompt:')
    print(prompt)
    raise e


