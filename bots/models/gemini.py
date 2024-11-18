from dotenv import load_dotenv
load_dotenv()
import os
from google.cloud import pubsub_v1
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as tf_text
import pandas
import time
import xgboost
import json
import shap
import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
from workers.pg.tasks import get_task, update_task_result


print('Starting predict_like worker...')


# GCP config
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
REGION = os.getenv('GCP_REGION')
SUBSCRIPTION_ID = 'predict_like_sub'

# Debug mode
DEBUG = False

# Load TensorFlow embedding models 
model_preprocess = 'https://tfhub.dev/tensorflow/bert_multi_cased_preprocess/3'
model_handle = 'https://tfhub.dev/tensorflow/bert_multi_cased_L-12_H-768_A-12/3'
bert_preprocess_model = hub.KerasLayer(model_preprocess)
bert_model = hub.KerasLayer(model_handle)
print('Tensorflow embedding models loaded.')

# Load Gambit model
model_source_h5 = 'nn_transformer_202405.h5' 
model_source_meta = 'nn_transformer_202405.json' 
worker_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(worker_dir, '../models/')
with open(model_dir + model_source_meta) as f:
    meta = json.load(f)
gambit = tf.keras.models.load_model(model_dir + model_source_h5)
print('Gambit model loaded.')
gambit.summary()

# Load XGBoost model
bird = xgboost.Booster() 
bird.load_model(model_dir + 'bird_0_0_1.xgb.json')
bird_explainer = shap.TreeExplainer(bird)
features = bird.feature_names
print('Bird model loaded.')
print('XGBoost features: ' + str(features))

# Configure Vertex model
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

def call_vertex_ai(prompt):
  try:
    responses = vertex_model.generate_content(
    [prompt],
    generation_config=generation_config,
    safety_settings=safety_settings)
    return responses.text
  except Exception as e:
    print(f"Error calling Vertex AI: {e}")
    return ''

feature_prompts = {
  'q_clear': ['make it more clear'],
  'q_audience': ['target a specific audience'],
  'q_info': ['make it more informative', 'make it less informative'],
  'q_easy': ['make it easier to understand'],
  'q_verifiable': ['make it based on a verifiable fact'],
  'q_personal': ['make it less personal', 'make it more personal'],
  'q_funny': ['make it more funny', 'make it less funny'],
  'q_meme_ref': ['introduce a well known meme'],
  'q_emo_res': ['trigger more emotional response', 'trigger less emotional response'],
  'q_happiness': ['make it happier', 'make it less happy'],
  'q_curiosity': ['trigger curiosity'],
  'q_aggressivity': ['make it more aggressive', 'make it less aggressive'],
  'q_surprise': ['introduce an element of surprise', 'make it less surprising'],
  'q_interesting_ask': ['ask an interesting question'],
  'q_call_action': ['add a call to action', 'remove any call to action']
}

def create_text_variations(text, change):
  candidates = []
  for f in change:
    for directive in feature_prompts[f]:
      prompt = "Write a variation of this tweet where you " + directive + ".\n"
      prompt += "Also, keep it as close as possible to the original text.\n"
      prompt += "--- Original Tweet ---\n"
      prompt += text
      prompt += "\n"
      prompt += "--- End of tweet ---\n"
      print(prompt)
      candidate = call_vertex_ai(prompt)
      print(candidate)
      if len(candidate)>0 and len(candidate)<340:
        candidates.append(candidate)
      print('*'*32)
  return candidates

print('Vertex AI ok.')


# Prediction function
def predict_and_explain(text_array):
  t0 = time.time()
  preprocessed = bert_preprocess_model(text_array)
  embed = bert_model(preprocessed)["pooled_output"]
  t1 = time.time()
  if DEBUG:
    print('embed', embed.shape, t1-t0)
  g = gambit.predict(embed)
  df0 = pandas.DataFrame({'text':text_array})
  df_q = pandas.DataFrame(g[0], columns=meta['questions'])
  df_cats = pandas.DataFrame(g[1], columns=meta['categories'])
  df_topics = pandas.DataFrame(g[2], columns=meta['topics'])
  df_encoder = pandas.DataFrame(g[4], columns=meta['encoder'])
  df = df0.join(df_q).join(df_cats).join(df_topics).join(df_encoder)
  t2 = time.time()
  if DEBUG:
    print('df', df.shape, t2-t1)
  df_features = df[features]
  dmatrix = xgboost.DMatrix(df_features)
  predict = bird.predict(dmatrix)
  t3 = time.time()
  if DEBUG:
    print('predict', predict, t3-t2)
  shap_values = bird_explainer(dmatrix)
  shap_values.feature_names = features  
  t4 = time.time()
  if DEBUG:
    print('shap_values', t4-t3)
  return predict, df_features, shap_values


def handle_message(message):
  if DEBUG:
    print('-'*32)
  print(f"Received message: {message.data}")
  message.ack()
  task_id = message.data.decode('utf-8')
  task = get_task(task_id)
  if not task:
    msg = f"No task found with ID: {task_id}"
    print(msg)
    result = {'error': msg}
    update_task_result(task_id, result)
  else:
    if DEBUG:
      print('Task: ' + str(task))
    request = task[4]
    text = request['text']
    if DEBUG:
      print('Text: ' + text)
    predict, df_features, shap_values = predict_and_explain([text])
    score = predict[0]
    if DEBUG:
      print('Score: ' + str(score))
    df_shap = pandas.DataFrame({
      'feature': features,
      'effect': shap_values[0].values
    })
    if DEBUG:
      print(df_shap)
    df_shap_improve =  df_shap[df_shap['effect']<0].sort_values('effect')
    try_change_feature = list(df_shap_improve['feature'])[:3]
    if DEBUG:
      print('Try change feature: ' + str(try_change_feature))
    candidates = create_text_variations(text, try_change_feature)
    if DEBUG:
      print('Candidates: ' + str(candidates))
    p2,_,_ = predict_and_explain(candidates)
    if DEBUG:
      print('p2: ' + str(p2))
    text_features = df_features.to_dict('records')[0]
    explain = df_shap.to_dict('records')
    result = {
      'text': text,
      'score': int(score*100),
      'features': text_features,
      'explain': explain,
      'candidates': candidates,
      'candidates_scores': [int(x*100) for x in p2.tolist()]
    }
    print(f"Task {task_id} completed with result: {result}")
    update_task_result(task_id, result)
  if DEBUG:
    print('-'*32)

def subscribe_to_pubsub():
  subscriber = pubsub_v1.SubscriberClient()
  subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
  streaming_pull_future = subscriber.subscribe(subscription_path, callback=handle_message)
  print(f"Listening for messages on {subscription_path}...")
  try:
    streaming_pull_future.result()
  except Exception as e:
    print(f"Listening for messages on {subscription_path} threw an exception: {e}.")
    streaming_pull_future.cancel()


if __name__ == "__main__":
    subscribe_to_pubsub()