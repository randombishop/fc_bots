from dotenv import load_dotenv
load_dotenv()
import os
import tensorflow as tf
import tensorflow_hub as hub
import sentencepiece as spm
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='tensorflow')


print('Loading Tensorflow models...')
model_dir = os.path.dirname(os.path.abspath(__file__))

sp = spm.SentencePieceProcessor()
spm_file = model_dir + '/tf_hub/uni-encoder-tf1-lite-v2/assets/universal_encoder_8k_spm.model'
sp.Load(spm_file)

model_handle = model_dir + '/tf_hub/uni-encoder-tf1-lite-v2'
bert_model = hub.load(model_handle).signatures['default']
print('Tensorflow embedding model loaded.')



def to_sparse_format(batch):
    """Convert a batch of tokenized sentences to sparse tensor format."""
    indices = []
    values = []
    for batch_idx, tokens in enumerate(batch):
        for token_idx, token in enumerate(tokens):
            indices.append([batch_idx, token_idx])
            values.append(token)
    indices = tf.constant(indices, dtype=tf.int64)
    values = tf.constant(values, dtype=tf.int64)
    dense_shape = tf.constant([len(batch), max(len(tokens) for tokens in batch)], dtype=tf.int64)
    return tf.sparse.SparseTensor(indices, values, dense_shape)


def preprocess(sentences):
  tokenized_sentences = [sp.encode_as_ids(sentence) for sentence in sentences]
  sparse_inputs = to_sparse_format(tokenized_sentences)
  return sparse_inputs


def bert(sentences):
  sparse_inputs = preprocess(sentences)
  e =  bert_model(
      values=sparse_inputs.values,
      indices=sparse_inputs.indices,
      dense_shape=sparse_inputs.dense_shape
  )
  return e['default'].numpy()

