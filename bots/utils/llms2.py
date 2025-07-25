from openai import OpenAI
import json5
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable
from vertexai.generative_models import GenerativeModel, Part
from vertexai import generative_models
from bots.utils.json_cleaner import clean_json


gemini_small = "gemini-2.0-flash-lite-001"
gemini_medium = "gemini-2.0-flash-001"
gemini_large = "gemini-2.5-flash"

def chat_llm(model):
  try:
    llm = ChatVertexAI(model=model, temperature=0, response_format="json")
    return llm
  except Exception as e:
    print(f'Error in create_llm: {e}')
    return None

def image_llm():
  try:
    llm_img = OpenAI().images
    return llm_img
  except Exception as e:
    print(f'Error in create_llm_image: {e}')
    return None

models = {
  'small': gemini_small,
  'medium': gemini_medium,
  'large': gemini_large
}

def get_max_capactity():
  return 50

def call_llm(size, prompt, instructions, schema):
  model = models[size]
  llm = ChatVertexAI(model=model, temperature=0, response_format="json")
  messages = [
    SystemMessage(instructions.encode('utf-8', errors='replace').decode('utf-8')),
    HumanMessage(prompt.encode('utf-8', errors='replace').decode('utf-8'))
  ]
  result = llm.invoke(messages)
  text = result.content
  text = clean_json(text)
  try:
    result = json5.loads(text)
  except:
    result = {}
  return result


def rewrite_prompt(original_prompt):
  try:
    messages = [
      SystemMessage("Rewrite the provided prompt to adhere to OpenAI's content policies."),
      HumanMessage(original_prompt)
    ]
    response = models['medium'].invoke(messages)
    return response.content if response else original_prompt
  except Exception as e:
    print('Failed to rewrite the prompt.')
    raise e

@traceable(run_type="llm", name="DallE3")
def _do_generate_image(prompt):
  model = image_llm()
  response = model.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1
  )
  return {'url': response.data[0].url, 'status': 'generated'}


def generate_image(prompt):
  try:
    result = _do_generate_image(prompt)
    return result['url']
  except Exception as e:
    if 'content_policy_violation' in str(e).lower():
      print('Content policy violation detected.')
      new_prompt = rewrite_prompt(prompt)
      result = _do_generate_image(new_prompt)
      return result['url']
    else: 
      raise e
    

@traceable(run_type="llm", name=gemini_small)
def call_llm_with_data(prompt, data, mime_type, instructions, schema):
  result = None
  try:
    image1 = Part.from_data(
      mime_type=mime_type,
      data=data,
    )
    vertex_model = GenerativeModel(
      gemini_small,
      system_instruction=instructions
    )
    generation_config = {
      "max_output_tokens": 1024
    }
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH
    }
    responses = vertex_model.generate_content(
      [prompt, image1],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True)
    text = ''
    for response in responses:
      t = response.text
      text += t
    text = clean_json(text)
    result = json5.loads(text)
  except Exception as e:
    print(f'Error in call_llm_with_data {e}')
    result = {}
  return result