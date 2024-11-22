from datetime import datetime, timedelta
from bots.data.wield import get_cast_info
from bots.data.dune import run_query
from bots.models.bert import bert
from bots.models.gambit import gambit, categories, topics
from dune_client.types import QueryParameter


def get_casts_for_fid(fid):
  query_id = 4248613
  params = [QueryParameter.number_type(name="fid", value=fid)]
  return run_query(query_id, params)

def get_top_casts(channel, keyword, category, max_rows):
  query_id = 4252915
  params = [
    QueryParameter.text_type(name="parent_url", value=channel if channel is not None else '*'),
    QueryParameter.text_type(name="keyword", value=keyword if keyword is not None else '*'),
    QueryParameter.text_type(name="category", value=category if category is not None else '*'),
    QueryParameter.number_type(name="limit", value=max_rows)
  ]
  return run_query(query_id, params)

def get_more_like_this(text, exclude_hash=None, limit=10):
  embedding = bert([text])
  features = gambit(embedding)
  features['category_label'] = features[categories].idxmax(axis=1)
  features['topic_label'] = features[topics].idxmax(axis=1)
  features = features.to_dict(orient='records')[0]
  features_q = [x for x in features.keys() if x.startswith('q_')]
  features_dim = [x for x in features.keys() if x.startswith('dim_')]
  query_id = 4302734
  params = [
    QueryParameter.text_type(name="category", value=features['category_label']),
    QueryParameter.text_type(name="topic", value=features['topic_label']),
    QueryParameter.number_type(name="limit", value=limit)
  ]
  for f in features_q+features_dim:
    params.append(QueryParameter.number_type(name=f, value=features[f]))
  if exclude_hash is not None:
    params.append(QueryParameter.text_type(name="exclude_hash", value=exclude_hash))
  return run_query(query_id, params)

def get_cast(hash):
  cast = get_cast_info(hash)
  return {
    'fid': int(cast['author']['fid']),
    'text': cast['text'],
    'mentions': cast['mentions'] if 'mentions' in cast else [], 
    'mentionsPos': cast['mentionsPositions'] if 'mentionsPositions' in cast else [],
    'parent_fid': cast['parentFid'] if 'parentFid' in cast else None,
    'parent_hash': cast['parentHash'] if 'parentHash' in cast else None
  }
  