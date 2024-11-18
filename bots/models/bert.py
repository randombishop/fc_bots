from dotenv import load_dotenv
load_dotenv()
import os
import tensorflow as tf
import tensorflow_text as tf_text


print('Loading Tensorflow models...')
model_dir = os.path.dirname(os.path.abspath(__file__))
model_preprocess = model_dir + '/tf_hub/bert-tensorflow2-en-uncased-preprocess-v3'
model_handle = model_dir + '/tf_hub/universal-sentence-encoder-tensorflow2-cmlm-en-base-v1'
bert_preprocess_model = tf.saved_model.load(model_preprocess)
bert_model = tf.saved_model.load(model_handle)
print('Tensorflow embedding model loaded.')


def bert(text_array):
  preprocessed = bert_preprocess_model(text_array)
  transformed = bert_model(preprocessed)
  print(transformed)
  return transformed['default']

