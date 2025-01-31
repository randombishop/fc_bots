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

def get_top_casts(channel, keyword, category, user_name, max_rows):
  query_id = 4252915
  params = [
    QueryParameter.text_type(name="parent_url", value=channel if channel is not None else '*'),
    QueryParameter.text_type(name="keyword", value=keyword if keyword is not None else '*'),
    QueryParameter.text_type(name="category", value=category if category is not None else '*'),
    QueryParameter.text_type(name="user_name", value=user_name if user_name is not None else '*'),
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

def format_when(timestamp):
  timestamp_seconds = int(timestamp) / 1000
  now = datetime.now()
  timestamp_dt = datetime.fromtimestamp(timestamp_seconds)
  delta = now - timestamp_dt
  if delta.days > 0:
    return f"{delta.days} days ago"
  hours = delta.seconds // 3600
  if hours > 0:
    return f"{hours} hours ago"
  minutes = delta.seconds // 60
  if minutes > 0:
    return f"{minutes} minutes ago"
  return "seconds ago"

def get_cast(hash):
  cast_info = get_cast_info(hash)
  if cast_info is None:
    return None
  cast = {
    'fid': int(cast_info['author']['fid']),
    'username': cast_info['author']['username'],
    'text': cast_info['text'],
    'mentions': cast_info['mentions'] if 'mentions' in cast_info else [], 
    'mentionsPos': cast_info['mentionsPositions'] if 'mentionsPositions' in cast_info else [],
    'parent_fid': cast_info['parentFid'] if 'parentFid' in cast_info else None,
    'parent_hash': cast_info['parentHash'] if 'parentHash' in cast_info else None,
    'timestamp': cast_info['timestamp'],
    'when': format_when(cast_info['timestamp'])
  }
  if 'embeds' in cast_info and 'quoteCasts' in cast_info['embeds'] and len(cast_info['embeds']['quoteCasts']) > 0:
      quote_cast = cast_info['embeds']['quoteCasts'][0]
      cast['quote'] = {'text': quote_cast['text'], 'fid': int(quote_cast['author']['fid']), 'username': quote_cast['author']['username']}
  return cast
  