from dotenv import load_dotenv
load_dotenv()
import os
import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
from workers.pg.tasks import get_task, update_task_result


print('Init Gemini model...')
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
REGION = os.getenv('GCP_REGION')
SUBSCRIPTION_ID = 'predict_like_sub'
vertexai.init(project=PROJECT_ID, location=REGION)
vertex_model = GenerativeModel("gemini-1.5-flash-001")
generation_config = {
    "max_output_tokens": 256,
    "temperature": 1,
    "top_p": 0.95,
}
safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}
print('Vertex AI model ready.')



def gemini(prompt):
  try:
    responses = vertex_model.generate_content(
      [prompt],
      generation_config=generation_config,
      safety_settings=safety_settings)
    return responses.text
  except Exception as e:
    print(f"Error calling Vertex AI: {e}")
    return ''
