from openai import OpenAI
import json5
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable
from bots.utils.json_cleaner import clean_json



def get_llm():
  model = "gemini-2.0-flash-001"
  llm = ChatVertexAI(model=model, safety_settings=[
    {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 4},
    {"category": "HARM_CATEGORY_TOXICITY", "threshold": 4},
    {"category": "HARM_CATEGORY_MEDICAL", "threshold": 4},
    {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 3},
    {"category": "HARM_CATEGORY_SEXUAL", "threshold": 2},
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 2}
  ])
  return llm


def get_llm_img():
  llm_img = OpenAI()
  return llm_img


def call_llm(llm, prompt, instructions, schema):
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


def rewrite_prompt(llm, original_prompt):
  try:
    messages = [
      SystemMessage("Rewrite the provided prompt to adhere to OpenAI's content policies."),
      HumanMessage(original_prompt)
    ]
    response = llm.invoke(messages)
    return response.content if response else original_prompt
  except Exception as e:
    print('Failed to rewrite the prompt.')
    raise e

@traceable(run_type="llm", name="DallE3")
def _do_generate_image(llm_img, prompt):
  response = llm_img.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1
  )
  return {'url': response.data[0].url, 'status': 'generated'}


def generate_image(llm_img, llm, prompt):
  try:
    result = _do_generate_image(llm_img, prompt)
    return result['url']
  except Exception as e:
    if 'content_policy_violation' in str(e).lower():
      print('Content policy violation detected.')
      new_prompt = rewrite_prompt(llm, prompt)
      result = _do_generate_image(llm_img, new_prompt)
      return result['url']
    else: 
      raise e