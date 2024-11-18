from dotenv import load_dotenv
load_dotenv()
import os
import tensorflow as tf
import tensorflow_text as tf_text
import tensorflow_hub as hub


print('Loading Tensorflow models...')
model_dir = os.path.dirname(os.path.abspath(__file__))
model_preprocess = model_dir + '/bert-tensorflow2-multi-cased-preprocess-v3'
model_handle = model_dir + '/https://tfhub.dev/tensorflow/bert_multi_cased_L-12_H-768_A-12/3'
bert_preprocess_model = tf.saved_model.load(model_preprocess)
bert_model = hub.KerasLayer(model_handle)
print('Tensorflow embedding model loaded.')


def bert(text_array):
  preprocessed = bert_preprocess_model(text_array)
  embed = bert_model(preprocessed)["pooled_output"]
  return embed

