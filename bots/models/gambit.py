from dotenv import load_dotenv
load_dotenv()
import os
import tensorflow as tf
import pandas
import json


print('Loading Gambit model...')
model_source_h5 = 'gambit2.h5' 
model_source_meta = 'gambit2.json' 
model_dir = os.path.dirname(os.path.abspath(__file__))
with open(model_dir  + '/' +  model_source_meta) as f:
  meta = json.load(f)
questions = meta['questions']
categories = meta['categories']
topics = meta['topics']
encoder = meta['encoder']
gambit_model = tf.keras.models.load_model(model_dir + '/' + model_source_h5)
print('Gambit model loaded.')
gambit_model.summary()


def gambit(input):
  g = gambit_model.predict(input)
  df_q = pandas.DataFrame(g[0], columns=meta['questions'])
  df_cats = pandas.DataFrame(g[1], columns=meta['categories'])
  df_topics = pandas.DataFrame(g[2], columns=meta['topics'])
  df_encoder = pandas.DataFrame(g[4], columns=meta['encoder'])
  df = df_q.join(df_cats).join(df_topics).join(df_encoder)
  return df
