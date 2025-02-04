import os
import time
import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models


USE_VERTEX_AI = os.getenv('USE_VERTEX_AI', "false")
#GEMINI_MODEL_NAME = 'gemini-2.0-flash-exp'
GEMINI_MODEL_NAME = 'gemini-1.5-flash-002'
MIN_DELAY = 3

if USE_VERTEX_AI == "true":
  print('Init Vertex AI...')
  vertexai.init(project=os.getenv('GCP_PROJECT_ID'), location=os.getenv('GCP_REGION'))
  print('Vertex AI ready.')
  

class GeminiLLM():
  
  def __init__(self):
    self.last_call = 0
    self.generation_config = {
      "max_output_tokens": 1024
    }
    self.safety_settings = {
      generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
      generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
      generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
      generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH
    }
    
  def query(self, prompt, instructions=None, schema=None):
    if time.time() - self.last_call < MIN_DELAY:
      delay = MIN_DELAY - (time.time() - self.last_call)
      print(f"Waiting {int(delay)} seconds to avoid rate limit...")
      time.sleep(delay)
    self.last_call = time.time()
    vertex_model = GenerativeModel(
      GEMINI_MODEL_NAME,
      system_instruction=instructions
    )
    responses = vertex_model.generate_content(
      [prompt],
      generation_config=self.generation_config,
      safety_settings=self.safety_settings,
      stream=True)
    text = ''
    for response in responses:
      t = response.text
      text += t
    return text

  

gemini = GeminiLLM()
